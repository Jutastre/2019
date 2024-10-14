import itertools
import math
import time

import intcodemachine as icm

INPUT_PATH = "input.txt"

def calculate_energy(moon):
    return sum(abs(n) for n in moon[0]) * sum(abs(n) for n in moon[1])

def main():

    with open(INPUT_PATH) as f:
        data = [int(n) for n in f.read().strip().split(",")]
    data[0] = 2
    icm.feed(data)
    icm.execute()
    screen = [[" " for _ in range(50)] for __ in range(25)]
    score = 0
    ball_position = 0
    paddle_position = 0
    while icm.status()[0] != 2:
        if icm.status()[0] == 3:
            icm.input(ball_position - paddle_position)
        x,y,tile_id = icm.output(),icm.output(),icm.output()
        if x == -1 and y == 0:
            score = tile_id
        else:
            match tile_id:
                case 0:
                    screen[y][x] = " "
                case 1:
                    screen[y][x] = "|"
                case 2:
                    screen[y][x] = "#"
                case 3:
                    paddle_position = x
                    screen[y][x] = "P"
                case 4:
                    ball_position = x
                    screen[y][x] = "¤"
        print(f"SCORE:{score}")
        for row in screen:
            print("".join(row))
        time.sleep(0.02)
    



if __name__ == "__main__":
    main()