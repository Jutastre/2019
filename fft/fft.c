#include <Python.h>
#include <stdio.h>

PyObject* fft(PyObject* self, PyObject* args) {
    PyObject* input_list;
    int phases;
    long offset;
    // printf("Parsing args...\n");

    if (!PyArg_ParseTuple(args, "Oil", &input_list, &phases, &offset)) {
        return NULL;
    }

    size_t list_size = (size_t)PyObject_Size(input_list);
    int* list;

    // printf("Mallocing list...\n");
    list = malloc(sizeof(int) * list_size);

    // printf("Populating list from python list...\n");
    // printf("[");
    for (size_t idx = 0; idx < list_size; idx++) {
        list[idx] = (int)PyLong_AsLong(PyList_GetItem(input_list, idx));
        // printf("%i, ", list[idx]);
    }
    // printf("]\n");

    // printf("Starting FFT...\n");
    for (size_t phase_idx = 0; phase_idx < phases; phase_idx++) {
        printf("Starting phase %lu...\n", phase_idx);
        for (size_t element_idx = offset; element_idx < list_size; element_idx++) {
            // printf("Starting element %lu...\n", element_idx);
            int value = 0;
            int flip = -1;
            for (size_t span_start_idx = element_idx; span_start_idx < list_size; span_start_idx += ((element_idx + 1) * 2)) {
                // printf("span_start_idx: %lu\n", span_start_idx);
                flip *= -1;
                for (size_t span_idx = 0; (span_idx < element_idx + 1) && ((span_start_idx + span_idx) < list_size); span_idx++) {
                    // printf("span_idx: %lu\n", span_idx);
                    value += flip * list[span_start_idx + span_idx];
                    // printf("value: %lu\n", value);
                }
                // printf("value: %i\n", value);
            }
            // printf("Result: %i\n", value);
            // printf("saving %i in element #%lu\n", abs(value) % 10, element_idx);
            list[element_idx] = abs(value) % 10;
        }
    }
    PyObject* output_list = Py_BuildValue("[]");
    for (size_t idx = 0; idx < list_size; idx++) {
        PyObject* value_to_append = PyLong_FromLong(list[idx]);
        PyList_Append(output_list, value_to_append);
        Py_DECREF(value_to_append);
    }
    free(list);
    return output_list;
}

static PyMethodDef methods[] = {
    {"fft", fft, METH_VARARGS, "FFT"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef fftmodule = {
    PyModuleDef_HEAD_INIT,
    "FFT Module",
    "The FFT Module made in C",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_fft() {
    return PyModule_Create(&fftmodule);
}