import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"
WALL = None



        

def main():
    with open(INPUT_PATH) as f:
        data = [int(n) for n in f.read().strip().split(",")]
    icm.feed(data)
    icm.execute()
    screen = [[" " for _ in range(80)] for __ in range(50)]
    x = 40
    y = 25
    recieved_code = 0
    while icm.status()[0] == 4:
        print(icm.output())
    while recieved_code != 2:
        command = input("command:")
        match command:
            case "1"|"w":
                command_code = 1
            case "2"|"s":
                command_code = 2
            case "3"|"a":
                command_code = 3
            case "4"|"d":
                command_code = 4
        icm.input(command_code)
        recieved_code = icm.output()
        if recieved_code == 0:
            match command_code:
                case 1:
                    screen[y - 1][x] = "#"
                case 2:
                    screen[y + 1][x] = "#"
                case 3:
                    screen[y][x - 1] = "#"
                case 4:
                    screen[y][x + 1] = "#"
        else:
            match command_code:
                case 1:
                    y -= 1
                case 2:
                    y += 1
                case 3:
                    x -= 1
                case 4:
                    x += 1

        screen[y][x] = "$"
        for row in screen:
            print("".join(row))
        screen[y][x] = "."



if __name__ == "__main__":
    main()