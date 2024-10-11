import itertools
import intcodemachine

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    for noun, verb in itertools.product(range(100), range(100)):


        data[1] = noun
        data[2] = verb

        intcodemachine.feed(data)
        intcodemachine.execute()
        output = intcodemachine.read()

        if output[0] == 19690720:
            print(f"answer:{100 * noun + verb}")
            break




if __name__ == "__main__":
    main()