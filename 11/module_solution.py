import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    icm.feed(data)
    icm.set_debug(3)
    hull = {}
    magic_set = set()
    direction = 0
    x = 0
    y = 0
    icm.execute()
    while icm.status()[0] != 2:
        icm.input(hull.get((x,y), 0))
        output = icm.output()
        hull[(x,y)] = output
        magic_set.add((x,y))
        direction = (direction + (1 if icm.output() else -1)) % 4
        match direction:
            case 0:
                x += 1
            case 1:
                y += 1
            case 2:
                x -= 1
            case 3:
                y -= 1
        print((x,y))
    # print(magic_set)
    map = [[" " for _ in range(150)] for _ in range(150)]

    for k,v in hull.items():
        map[k[0] + 50][k[1] + 50] = v

    painted_map = "".join("".join(str(num) for num in row) for row in map)



    for row in map:
        print("".join(str(num) for num in row))
        # print("".join(str(num) for num in row).replace("0", " "))

    answer = None
    print(f"answer: {len(magic_set)}")
    print(f'answer2: {painted_map.count("1") + painted_map.count("0")}')



if __name__ == "__main__":
    main()