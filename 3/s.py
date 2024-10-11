import itertools

INPUT_PATH = "input.txt"

def manhattan(target:tuple[int,int], source:tuple[int,int] = (0,0)):
    return abs(source[0] - target[0]) + abs(source[1] - target[1])

def draw_wire(input:str):
    moves = input.split(",")
    x=0
    y=0
    points =  {}
    counter = 0

    for move in moves:
        direction = move[0]
        distance = int(move[1:])
        while distance > 0:
            match direction:
                case 'U':
                    y -= 1
                case 'D':
                    y += 1
                case 'L':
                    x -= 1
                case 'R':
                    x += 1
            distance -= 1
            counter += 1
            points[(x,y)]  = counter
    print("wire drawn")
    return points


def main():
    file = open(INPUT_PATH)
    data = file.read().strip().split("\n")
    wires = [draw_wire(wire) for wire in data]
    intersections = []
    for coords in (wires[0].keys() & wires[1].keys()):
        intersections.append(wires[0][coords] + wires[1][coords])
    #print(intersections)
    print(min(intersections))


if __name__ == "__main__":
    main()