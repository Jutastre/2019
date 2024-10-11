import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    icm.feed(data)

    hull = {}
    direction = 0
    


    answer = None
    print(f"answer: {answer}")



if __name__ == "__main__":
    main()