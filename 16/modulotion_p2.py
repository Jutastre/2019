import itertools
import math
import time

import fft

# import intcodemachine as icm

INPUT_PATH = "input.txt"



def main():
    with open(INPUT_PATH) as f:
        data = [int(char) for char in f.read().strip().split("\n")[0]]
    # real_signal = [a for a in itertools.repeat(data, 10000)]
    real_signal = data * 10_000
    message_offset = int(''.join([str(number) for number in data[:7]]))
    # print(f"real_signal: {real_signal}")

    solved_signal = fft.fft(real_signal, 100, message_offset)

    print(f"old: {''.join([str(number) for number in solved_signal[:8]])}")
    print(f"answer: {''.join([str(number) for number in solved_signal[message_offset:message_offset + 8]])}")


if __name__ == "__main__":
    main()
