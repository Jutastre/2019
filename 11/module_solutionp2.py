import itertools
import math
# import intcodemachine as icm

INPUT_PATH = "input.txt"
ORIGIN = 13,17
TARGET = 200

def find_visible(data):

    col,row = ORIGIN
    tdata = [[c for c in r] for r in data]
    tdata[row][col] = "*"
    for tcol,trow in itertools.product(range(len(data[0])),range(len(data))):
        if tdata[trow][tcol] == '#':
            xdiff = tcol - col
            ydiff = trow - row
            div = math.gcd(xdiff,ydiff)
            xdir = int(xdiff / div)
            ydir = int(ydiff / div)
            if xdiff == 0 and ydiff == 0:
                continue
            xdiff += xdir
            ydiff += ydir
            while (0 <= col + xdiff < len(data[0])) and (0 <= row + ydiff < len(data)):
                tdata[row + ydiff][col + xdiff] = "."
                xdiff += xdir
                ydiff += ydir
    visible = "".join("".join(row) for row in tdata).count("#")
    vmap = [[c for c in r] for r in tdata]
    return visible, vmap

def zap_from_map(data,zapmap):
    for col,row in itertools.product(range(len(data[0])),range(len(data))):
        if zapmap[row][col] == "#":
            data[row][col] = "."

def get_angles(map, origin):
    returntuples = []
    xori, yori = ORIGIN
    for col,row in itertools.product(range(len(map[0])),range(len(map))):
        if map[row][col] == "#":
            angle = -math.atan2((col - xori), (row - yori))
            returntuples.append(((col,row), angle))
    return returntuples

def sortfunction(tuppp):
    return tuppp[1]

def main():
    with open(INPUT_PATH) as f:
        data = [[char for char in row] for row in f.read().strip().split("\n")]

    zapped = 0

    while zapped < TARGET:
        zap, map = find_visible(data)
        zapped += zap
        zap_from_map(data,map)
    for n in range(len(map)):
        print(f"{map[n]}")

    final_batch = get_angles(map, ORIGIN)
    sorted_batch = sorted(final_batch, key=sortfunction)
    for a in sorted_batch:
        print(a)
    answer = sorted_batch[(TARGET-1) - (zapped - zap)][0]


    print(f"answer: {answer}")



if __name__ == "__main__":
    main()