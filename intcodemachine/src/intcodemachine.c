#include <Python.h>
#include <stdio.h>

#define NUMBER_OF_MACHINES 32
#define MEMORY_SIZE (256*4*16)

enum Status {
    STATUS_NOT_LOADED,
    STATUS_READY,
    STATUS_HALTED,
    STATUS_AWAITING_INPUT,  // making these match the opcodes
    STATUS_AWAITING_OUTPUT, //
};


struct Virtual_machine {
    long long* tape;
    size_t tapesize;
    enum Status status;

    size_t program_counter;
    size_t relative_base;

    size_t io_location;
    size_t debug_level;
};

static long long* tape;
static size_t machine_selector;

static struct Virtual_machine machines[NUMBER_OF_MACHINES];

static struct Virtual_machine* machine;


// enum MODE {
//     MODE_RELATIVE,
//     MODE_IMMEDIATE
// };

// enum MODE mode = MODE_RELATIVE;


// enum Status status = STATUS_NOT_LOADED;

static void _debug_print_tape() {
    printf("dbg: [");
    for (size_t idx = 0; idx < machine->tapesize; idx++) {
        printf("%lli, ", tape[idx]);
    }
    printf("]\n");
}

static bool set_tapesize(size_t target_size) {
    if (tape) {
        free(tape);
    }
    tape = malloc(sizeof(long long) * target_size);
    if (!tape) {
        PyErr_SetString(PyErr_NoMemory(), "Allocating memory for tape failed");
        return true;
    }
    machine->tapesize = target_size;
    machine->tape = tape;
    return false;
}



static PyObject* select_machine(PyObject* self, PyObject* args) {
    char error_msg_buffer[256];
    int target;
    PyArg_ParseTuple(args, "i", &target);
    if (machine->debug_level >= 1) printf("Selecting machine #%i\n", target);
    if ((target < 0) || (target > NUMBER_OF_MACHINES)) {
        sprintf(error_msg_buffer, "Invalid machine selection (tried selecting %i; not in range 0 to %i inclusive)", target, NUMBER_OF_MACHINES - 1);
        PyErr_SetString(PyExc_ValueError, error_msg_buffer);
        return NULL;
    }

    machine_selector = target;
    machine = &machines[machine_selector];
    tape = machine->tape;


    Py_RETURN_NONE;
}

static bool _execute() {
    long long left_operand;
    long long right_operand;
    long long target;
    char error_msg_buffer[256];
    while (true) {
        long long opcode = tape[machine->program_counter] % 100;
        int modes = tape[machine->program_counter] / 100;
        int mode_vector[3];
        mode_vector[0] = modes % 10;
        mode_vector[1] = (modes / 10) % 10;
        mode_vector[2] = (modes / 100) % 10;
        if (machine->debug_level >= 4) _debug_print_tape();
        if (machine->debug_level >= 3) printf("Decoding instruction: %lli\n", tape[machine->program_counter]);
        if (machine->debug_level >= 2) printf("Executing opcode: %lli @ %lu\n", opcode, machine->program_counter);
        if (machine->debug_level >= 3) printf("Using mode: %i\n", modes);
        if (machine->program_counter >= machine->tapesize) {
            sprintf(error_msg_buffer, "Tried to execute out of bounds opcode @%lu; tape is only %lu", machine->program_counter, machine->tapesize);
            PyErr_SetString(PyExc_ValueError, "Program reached OOB");
            return true;
        }
        switch (opcode) {
            case 1:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];
                target = tape[machine->program_counter + 3];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }
                if (mode_vector[2] == 2) {
                    target += machine->relative_base;
                }

                tape[target] = left_operand + right_operand;
                if (machine->debug_level >= 3) printf("%lli + %lli = %lli\n", left_operand, right_operand, tape[target]);

                machine->program_counter += 4;
                break;

            case 2:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];
                target = tape[machine->program_counter + 3];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }
                if (mode_vector[2] == 2) {
                    target += machine->relative_base;
                }

                tape[target] = left_operand * right_operand;
                if (machine->debug_level >= 3) printf("%lli * %lli = %lli\n", left_operand, right_operand, tape[target]);

                machine->program_counter += 4;
                break;

            case 3:
                left_operand = tape[machine->program_counter + 1];

                if (mode_vector[0] == 2) {
                    left_operand += machine->relative_base;
                }

                machine->status = STATUS_AWAITING_INPUT;
                machine->io_location = left_operand;
                machine->program_counter += 2;
                return false;

            case 4:
                left_operand = tape[machine->program_counter + 1];

                if (mode_vector[0] == 1) {
                    left_operand = machine->program_counter + 1;
                }
                if (mode_vector[0] == 2) {
                    left_operand += machine->relative_base;
                }

                machine->status = STATUS_AWAITING_OUTPUT;
                machine->io_location = left_operand;
                machine->program_counter += 2;
                return false;

            case 5:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }

                if (left_operand != 0) {
                    machine->program_counter = right_operand;
                }
                else {
                    machine->program_counter += 3;
                }
                break;

            case 6:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }

                if (left_operand == 0) {
                    machine->program_counter = right_operand;
                }
                else {
                    machine->program_counter += 3;
                }
                break;

            case 7:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];
                target = tape[machine->program_counter + 3];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }
                if (mode_vector[2] == 2) {
                    target += machine->relative_base;
                }

                if (left_operand < right_operand) {
                    tape[target] = 1;
                }
                else {
                    tape[target] = 0;
                }
                machine->program_counter += 4;
                break;

            case 8:
                left_operand = tape[machine->program_counter + 1];
                right_operand = tape[machine->program_counter + 2];
                target = tape[machine->program_counter + 3];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }
                if (mode_vector[1] == 0) {
                    right_operand = tape[right_operand];
                }
                else if (mode_vector[1] == 2) {
                    right_operand = tape[right_operand + machine->relative_base];
                }
                if (mode_vector[2] == 2) {
                    target += machine->relative_base;
                }

                if (left_operand == right_operand) {
                    tape[target] = 1;
                }
                else {
                    tape[target] = 0;
                }
                machine->program_counter += 4;
                break;

            case 9:
                left_operand = tape[machine->program_counter + 1];

                if (mode_vector[0] == 0) {
                    left_operand = tape[left_operand];
                }
                else if (mode_vector[0] == 2) {
                    left_operand = tape[left_operand + machine->relative_base];
                }

                machine->relative_base += left_operand;
                if (machine->debug_level >= 3) printf("relative_base set to %lu\n", machine->relative_base);
                machine->program_counter += 2;
                break;

            case 99:
                machine->status = STATUS_HALTED;
                return false;

            default:
                sprintf(error_msg_buffer, "Unknown opcode: %lli @ %lu", tape[machine->program_counter], machine->program_counter);
                PyErr_SetString(PyExc_ValueError, "Unknown opcode");
                return true;
        }
    }
}

static PyObject* feed_tape(PyObject* self, PyObject* arg) {
    PyObject* tape_list;
    if (!PyArg_Parse(arg, "O", &tape_list)) {
        return NULL;
    }
    size_t fed_tape_size = (size_t)PyObject_Size(tape_list);
    size_t internal_memory_size = MEMORY_SIZE;
    if (set_tapesize(internal_memory_size)) {
        return NULL;
    }
    for (size_t idx = 0; idx < internal_memory_size; idx++) {
        if (idx < fed_tape_size) {
            tape[idx] = PyLong_AsLongLong((PyList_GetItem(tape_list, idx)));
        }
        else {
            tape[idx] = 0;
        }
    }

    machine->program_counter = 0;
    machine->relative_base = 0;
    machine->status = STATUS_READY;

    if (machine->debug_level >= 1) printf("Finished feeding tape\n");
    if (machine->debug_level >= 2) printf("Memory size now %lu\n", machine->tapesize);

    Py_RETURN_NONE;
}

static PyObject* set_debug(PyObject* self, PyObject* arg) {
    int value;
    if (!PyArg_Parse(arg, "i", &value)) {
        return NULL;
    }
    machine->debug_level = value;
    printf("Debug level of machine #%lu set to %lu\n", machine_selector, machine->debug_level);
    Py_RETURN_NONE;
}
static PyObject* set_debug_global(PyObject* self, PyObject* arg) {
    int value;
    if (!PyArg_Parse(arg, "i", &value)) {
        return NULL;
    }
    for (size_t idx = 0; idx < NUMBER_OF_MACHINES; idx++) {
        machines[idx].debug_level = value;
    }
    printf("Debug level of all machines set to %lu\n", machine->debug_level);
    Py_RETURN_NONE;
}

static PyObject* reset_machine(PyObject* self, PyObject* args) {
    if (machine->debug_level >= 1) printf("Resetting machine\n");
    machine->program_counter = 0;
    machine->relative_base = 0;
    machine->status = STATUS_READY;
    Py_RETURN_NONE;
}

static PyObject* execute(PyObject* self, PyObject* args) {
    if (machine->status != STATUS_READY) {
        PyErr_SetString(PyExc_ValueError, "Error! Not ready");
        return NULL;
    }
    if (machine->debug_level >= 1) printf("Beginning execution\n");
    if (machine->debug_level >= 4) _debug_print_tape();
    if (_execute()) {
        return NULL;
    }
    if (machine->debug_level >= 4) _debug_print_tape();
    if (machine->debug_level >= 2) printf("Finished execution\n");
    Py_RETURN_NONE;
}

static PyObject* read_tape(PyObject* self, PyObject* args) {
    PyObject* tape_list = Py_BuildValue("[]");
    for (size_t idx = 0; idx < machine->tapesize; idx++) {
        PyObject* value_to_append = PyLong_FromLongLong(tape[idx]);
        PyList_Append(tape_list, value_to_append);
        Py_DECREF(value_to_append);
    }
    return tape_list;
}

static PyObject* input(PyObject* self, PyObject* arg) {
    if (machine->status != STATUS_AWAITING_INPUT) {
        char error_string_buffer[256];
        sprintf(error_string_buffer, "Error! Unexpected input (Status is %i)", machine->status);
        PyErr_SetString(PyExc_ValueError, error_string_buffer);
        return NULL;
    }
    long long input_value;
    if (!PyArg_Parse(arg, "L", &input_value)) {
        return NULL;
    }
    if (machine->debug_level >= 1) printf("Inputting value %lli to address %lu\n", input_value, machine->io_location);
    tape[machine->io_location] = input_value;
    if (machine->debug_level >= 2) printf("Resuming execution\n");
    if (_execute()) {
        return NULL;
    }
    if (machine->debug_level >= 2) printf("Finished execution\n");
    Py_RETURN_NONE;
}

static PyObject* output(PyObject* self, PyObject* args) {
    if (machine->status != STATUS_AWAITING_OUTPUT) {
        char error_string_buffer[256];
        sprintf(error_string_buffer, "Error! Unexpected output (Status is %i)", machine->status);
        PyErr_SetString(PyExc_ValueError, error_string_buffer);
        return NULL;
    }
    // if (machine->debug_level >= 1) printf("Outputting from address %lu\n", machine->io_location);
    if (machine->debug_level >= 1) printf("Outputting value %lli from address %lu\n", tape[machine->io_location], machine->io_location);
    PyObject* output_value = PyLong_FromLongLong(tape[machine->io_location]);
    if (machine->debug_level >= 2) printf("Resuming execution\n");
    if (_execute()) {
        return NULL;
    }
    if (machine->debug_level >= 2) printf("Finished execution\n");
    return output_value;
}
static PyObject* get_status(PyObject* self, PyObject* args) {
    char string_buffer[256];

    switch (machine->status) {
        case STATUS_NOT_LOADED:
            sprintf(string_buffer, "STATUS_NOT_LOADED");
            break;
        case STATUS_READY:
            sprintf(string_buffer, "STATUS_READY");
            break;
        case STATUS_AWAITING_INPUT:
            sprintf(string_buffer, "STATUS_AWAITING_INPUT");
            break;
        case STATUS_AWAITING_OUTPUT:
            sprintf(string_buffer, "STATUS_AWAITING_OUTPUT");
            break;
        case STATUS_HALTED:
            sprintf(string_buffer, "STATUS_HALTED");
            break;
    }
    return Py_BuildValue("[is]", machine->status, string_buffer);
}

static PyMethodDef methods[] = {
    {"reset", reset_machine, METH_NOARGS, "Select which machine to operate"},
    {"select_machine", select_machine, METH_VARARGS, "Select which machine to operate"},
    {"set_debug", set_debug, METH_O, "Sets debug printing level"},
    {"set_debug_global", set_debug_global, METH_O, "Sets debug printing on/off for all machines"},
    {"status", get_status, METH_NOARGS, "Reads the machines current status"},
    {"feed", feed_tape, METH_O, "Feeds a program into the machine"},
    {"execute", execute, METH_NOARGS, "Executes the program in the machine"},
    {"read", read_tape, METH_NOARGS, "Reads the memory of the machine"},
    {"output", output, METH_NOARGS, "Retrieves output"},
    {"input", input, METH_O, "Sends input"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef intcodemachine = {
    PyModuleDef_HEAD_INIT,
    "VirtualIntcodeMachine",
    "The IntCodeMachine made in C",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_intcodemachine() {
    machine_selector = 0;
    machine = &machines[machine_selector];

    for (size_t idx = 0; idx < NUMBER_OF_MACHINES; idx++) {
        machines[idx].tapesize = 0;
        machines[idx].status = STATUS_NOT_LOADED;
    }

    machine->debug_level = 0;
    tape = machine->tape;

    return PyModule_Create(&intcodemachine);
}
