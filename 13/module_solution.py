import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"

def calculate_energy(moon):
    return sum(abs(n) for n in moon[0]) * sum(abs(n) for n in moon[1])

def main():
    with open(INPUT_PATH) as f:
        data = [int(n) for n in f.read().strip().split(",")]
    icm.feed(data)
    icm.execute()
    screen = {}
    score = 0
    while icm.status()[0] != 2:
        x,y,tile_id = icm.output(),icm.output(),icm.output()
        if x == -1 and y == 0:
            score = tile_id
        if tile_id:
            screen[(x,y)] = tile_id
        else:
            screen.pop((x,y), None)
    print(f"values: {screen.values()}")
    print(f"values: {list(screen.values())}")
    print(f"answer: {list(screen.values()).count(2)}")



if __name__ == "__main__":
    main()