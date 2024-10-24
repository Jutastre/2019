import itertools
import math
import icm

INPUT_PATH = "input.txt"

DRAW_MARGIN = 25

program = ""


def scan_point(x, y):
    icm.feed(program)
    icm.execute()
    icm.input(x)
    icm.input(y)
    return icm.output() == 1


def scan_square(x, y, size):
    for sy in range(y, y + size):
        for sx in range(x, x + size):
            if not scan_point(sx, sy):
                return False
    return True


def draw_square(x, y, size):
    for sy in range(y - DRAW_MARGIN, y + size + DRAW_MARGIN):
        for sx in range(x - DRAW_MARGIN, x + size + DRAW_MARGIN):
            if not scan_point(sx, sy):
                print(" ", end="")
            else:
                if ((sx >= x) and (sx < x + size)) and ((sy >= y) and (sy < y + size)):
                    print("O", end="")
                else:
                    print("#", end="")
        print()
    return True


def main():
    with open(INPUT_PATH) as f:
        global program
        program = [int(n) for n in f.read().strip().split(",")]
    x = 0
    y = 0
    size = 100
    while not scan_square(x, y, size) and x < 500 and y < 500:
        if not scan_point(x + size, y):
            y += 1
        elif not scan_point(x, y + size):
            x += 1

    while not scan_square(x, y, size):
        if not scan_point(x + size, y):
            y += 10
        elif not scan_point(x, y + size):
            x += 10

    x -= 10
    y -= 10

    while not scan_square(x, y, size):
        if not scan_point(x, y + size):
            x += 1
        elif not scan_point(x + size, y):
            y += 1
    oldx = 0
    oldy = 0
    while (oldx != x) or (oldy != y):
        oldx = x
        oldy = y
        for negx, negy in itertools.product(range(20), range(20)):
            if negx == 0 and negy == 0:
                continue
            if scan_square(x - negx, y - negy, size):
                x -= negx
                y -= negy
                break

    # assert scan_square(x, y, size)
    # assert not scan_square(x - 1, y, size)
    # assert not scan_square(x, y - 1, size)
    # assert not scan_square(x - 1, y - 1, size)

    draw_square(x, y, size)

    print(f"answer: {(x * 10000) + y}")


if __name__ == "__main__":
    main()
