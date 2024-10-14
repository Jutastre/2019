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
    # real_signal = [a for a in itertools.repeat(data, 10000)]
    real_signal = data * 10_0
    message_offset = int(''.join([str(number) for number in data[:7]]))
    print(f"offset: {message_offset}")
    for phase in range(100):
        print(f"phase: {phase}")
        new_data = []
        for element_id, _ in enumerate(real_signal):
            if (element_id % 10_0) == 0:
                print(f"element_id: {element_id}")
            value_sum = 0
            pattern = get_element_pattern(element_id)
            flip_flop = -1
            for n in range(1, len(real_signal), 2):
                flip_flop *= -1
                value_sum += sum(real_signal[((element_id + 1) * n) - 1 : ((element_id + 1) * (n + 1)) - 1]) * flip_flop
                # value_sum %= 10
                if ((element_id * (n + 1)) - 1) >= len(real_signal):
                    break
            new_data.append(abs(value_sum) % 10)
        real_signal = new_data

    print(f"old: {''.join([str(number) for number in real_signal[:8]])}")
    print(f"answer: {''.join([str(number) for number in real_signal[message_offset:message_offset + 8]])}")


if __name__ == "__main__":
    main()
