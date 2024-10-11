import itertools
import math
# import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [[char for char in row] for row in f.read().strip().split("\n")]

    answer = 0
    location = None

    for col,row in itertools.product(range(len(data[0])),range(len(data))):
        if data[row][col] == "#":
            print(f"trying {(col,row)}")
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
                        # print("a")
                        tdata[row + ydiff][col + xdiff] = "."
                        xdiff += xdir
                        ydiff += ydir
            visible = "".join("".join(row) for row in tdata).count("#")
            print(f"visible: {visible}")
            if visible > answer:
                for n in range(len(data)):
                    print(f"{tdata[n]}")
                answer = max(answer,visible)
                location = (col,row)




    print(f"answer: {answer}")
    print(f"location: {location}")



if __name__ == "__main__":
    main()