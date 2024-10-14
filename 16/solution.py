import itertools
import math
import time

# import intcodemachine as icm

INPUT_PATH = "input.txt"


def get_element_pattern(element_index):
    base_pattern = [0, 1, 0, -1]
    output = []
    for value in base_pattern:
        output = output + [a for a in itertools.repeat(value, element_index + 1)]
    return output

def skip(iterator):
    try:
        next(iterator)
        yield from iterator
    except StopIteration:
        return

def main():
    with open(INPUT_PATH) as f:
        data = [int(char) for char in f.read().strip().split("\n")[0]]
    # print(data)
    for _ in range(100):
        new_data = []
        for element_id, _ in enumerate(data):
            value_sum = 0
            pattern = get_element_pattern(element_id)
            for a, b in zip(data, skip(itertools.cycle(pattern))):
                value_sum += a * b
            new_data.append(abs(value_sum) % 10)
        data = new_data

    print(f"answer: {''.join([str(number) for number in data[:8]])}")


if __name__ == "__main__":
    main()
