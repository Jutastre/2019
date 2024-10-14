import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"

def main():
    if INPUT_PATH[0] != "t":
        with open(INPUT_PATH) as f:
            program = [int(n) for n in f.read().strip().split(",")]
        icm.feed(program)
        icm.execute()
        raw_data = []
        while icm.status()[0] != 2:
            raw_data.append(icm.output())
        data = bytearray(raw_data).decode().strip().split("\n")
    else:
        with open(INPUT_PATH) as f:
            data = [row for row in f.read().strip().split("\n")]
    
    for row in data:
        print(row)

    crossings = []
    for x,y in itertools.product(range(len(data[0])),range(len(data))):
        if data[y][x] == ".":
            continue
        if x != 0 and data[y][x-1] == ".":
            continue
        if y != 0 and data[y-1][x] == ".":
            continue
        if x != len(data[0]) - 1 and data[y][x + 1] == ".":
            continue
        if y != len(data) - 1 and data[y + 1][x] == ".":
            continue
        crossings.append((x,y))
    print(f"crossings: {crossings}")
    print(f"answer: {sum(x*y for x,y in crossings)}")


if __name__ == "__main__":
    main()
