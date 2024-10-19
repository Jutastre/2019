import itertools
import math
import icm

INPUT_PATH = "input.txt"

def move_forward(state):
    position, direction, data = state
    x,y = position
    match direction:
        case "^":
            y -= 1
        case "v":
            y += 1
        case "<":
            x -= 1
        case ">":
            x += 1
    state[0] = (x,y)

def look_forward(state):
    position, direction, data = state
    x,y = position
    match direction:
        case "^":
            y -= 1
        case "v":
            y += 1
        case "<":
            x -= 1
        case ">":
            x += 1
    if any((x < 0, y < 0, x >= len(data[0]), y >= len(data))):
        return '.'
    return data[y][x]

def look_left(state):
    position, direction, data = state
    x,y = position
    match direction:
        case ">":
            y -= 1
        case "<":
            y += 1
        case "^":
            x -= 1
        case "v":
            x += 1
    if any((x < 0, y < 0, x >= len(data[0]), y >= len(data))):
        return '.'
    return data[y][x]
def look_right(state):
    position, direction, data = state
    x,y = position
    match direction:
        case "<":
            y -= 1
        case ">":
            y += 1
        case "v":
            x -= 1
        case "^":
            x += 1
    if any((x < 0, y < 0, x >= len(data[0]), y >= len(data))):
        return '.'
    return data[y][x]

def turn_left(state):
    position, direction, data = state
    x,y = position
    match direction:
        case "<":
            direction = "v"
        case ">":
            direction = "^"
        case "v":
            direction = ">"
        case "^":
            direction = "<"
    state[1] = direction

def turn_right(state):
    position, direction, data = state
    x,y = position
    match direction:
        case "<":
            direction = "^"
        case ">":
            direction = "v"
        case "v":
            direction = "<"
        case "^":
            direction = ">"
    state[1] = direction



def look_left(state):
    position, direction, data = state
    x,y = position
    turn_left(state)
    result = look_forward(state)
    turn_right(state)
    return result
def look_right(state):
    position, direction, data = state
    x,y = position
    turn_right(state)
    result = look_forward(state)
    turn_left(state)
    return result

# def look_left(state):
#     position, direction, data = state
#     x,y = position
#     match direction:
#         case ">":
#             y -= 1
#         case "<":
#             y += 1
#         case "^":
#             x -= 1
#         case "v":
#             x += 1
#     if any(x < 0, y < 0, x > len(data[0]), y > len(data)):
#         return '.'
#     return data[y][x]
# def look_right(state):
#     position, direction, data = state
#     x,y = position
#     match direction:
#         case "<":
#             y -= 1
#         case ">":
#             y += 1
#         case "v":
#             x -= 1
#         case "^":
#             x += 1
#     if any(x < 0, y < 0, x > len(data[0]), y > len(data)):
#         return '.'
#     return data[y][x]



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

    program[0] = 2

    icm.feed(program)
    icm.execute()

    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char != '#' and char != '.':
                direction = char
                position = (x,y)
    print(f"dir: {direction}, position: {position}")
    state = [position, direction, data]
    sequence = []
    while any((look_forward(state) == '#',look_left(state) == '#',look_right(state) == '#')):
        if look_forward(state) == '#':
            #sequence[-1] += 1
            sequence.append("F")
            move_forward(state)
        elif look_left(state) == "#":
            turn_left(state)
            # sequence[-1] = str(sequence[-1])
            sequence.append("L")
            # sequence.append(0)
        else:
            turn_right(state)
            # sequence[-1] = str(sequence[-1])
            sequence.append("R")
            # sequence.append(0)
            
    # sequence[-1] = str(sequence[-1])
    print("".join(sequence) + ",")


if __name__ == "__main__":
    main()
