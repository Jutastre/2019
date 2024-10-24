import itertools
import math
import icm

INPUT_PATH = "input.txt"

def main():
    with open(INPUT_PATH) as f:
        program = [int(n) for n in f.read().strip().split(",")]
    answer = 0
    for x,y in itertools.product(range(50), range(50)):
        icm.feed(program)
        icm.execute()
        icm.input(x)
        icm.input(y)
        answer += icm.output()

    print(f"answer: {answer}")


if __name__ == "__main__":
    main()
