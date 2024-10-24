import itertools
import math
import icm

INPUT_PATH = "input.txt"

def input_ascii(string:str):
    for byte in string.encode():
        icm.input(byte)

def read_output():
    buffer = bytearray()
    while icm.status()[0] == 4:
        buffer.append(icm.output())
    print(buffer.decode())

def main():
    with open(INPUT_PATH) as f:
        program = [int(n) for n in f.read().strip().split(",")]
    icm.set_debug(0)
    icm.feed(program)
    icm.execute()
    string = "NOT B J\nWALK\n"
    read_output()
    input_ascii(string)
    read_output()

    # print(f"answer: {answer}")


if __name__ == "__main__":
    main()
