import itertools

INPUT_PATH = "input.txt"


def main():
    print(list(range(100)))
    file = open(INPUT_PATH)
    data = file.read().strip().split(",")
    for noun,verb in itertools.product(range(100),range(100)):
        tape = [int(value) for value in data]
        tape[1] = noun
        tape[2] = verb
        prc = 0
        while tape[prc] != 99:

            match tape[prc]:
                case 1:
                    tape[tape[prc+3]] = tape[tape[prc+1]] + tape[tape[prc+2]] #add
                    prc += 4
                case 2:
                    tape[tape[prc+3]] = tape[tape[prc+1]] * tape[tape[prc+2]] #mul
                    prc += 4
        
        if tape[0] == 19690720:
            print(tape[0])
            print(noun)
            print(verb)

if __name__ == "__main__":
    main()