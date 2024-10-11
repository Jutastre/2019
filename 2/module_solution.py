import itertools
import intcodemachine

INPUT_PATH = "input.txt"


def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    data[1] = 12
    data[2] = 2

    intcodemachine.feed(data)
    intcodemachine.execute()
    output = intcodemachine.read()

    print(f"answer:{output[0]}")



if __name__ == "__main__":
    main()