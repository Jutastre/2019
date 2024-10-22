import itertools
import math
import icm

INPUT_PATH = "input.txt"
DEBUG_LEVEL = 0

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

def raw_sequence_to_input_string(string:str) -> str:
    sequence = []
    while len(string) > 0:
        match string[0]:
            case "L":
                sequence.append("L")
            case "R":
                sequence.append("R")
            case "F":
                if isinstance(sequence[-1], int):
                    sequence[-1] += 1
                else:
                    sequence.append(1)
        string = string[1:]
    sequence = [str(ch) for ch in sequence]
    return ",".join(sequence)


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

    icm.set_debug(DEBUG_LEVEL)
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
    sequence_string = "".join(sequence)
    print(sequence_string)

    for size1,size2,size3 in itertools.product(range(10,40),range(10,40),range(10,40)):
        try:
            first_substring = sequence_string[:size1]
            first_index = 0
            idx = size1
            while (sequence_string[idx:idx+size1] == first_substring):
                idx += size1
            if idx > len(sequence_string):
                continue
            second_substring = sequence_string[idx:idx+size2]
            second_index = idx
            idx = idx+size2
            while ((first_condition := (sequence_string[idx:idx+size1] == first_substring)) or (sequence_string[idx:idx+size2] == second_substring)):
                if first_condition:
                    idx += size1
                else:
                    idx += size2
            if idx > len(sequence_string):
                continue
            third_substring = sequence_string[idx:idx+size3]
            third_index = idx
            while idx < len(sequence_string) and ((first_condition := (sequence_string[idx:idx+size1] == first_substring)) or (second_condition := (sequence_string[idx:idx+size2] == second_substring)) or (sequence_string[idx:idx+size3] == third_substring)):
                if first_condition:
                    idx += size1
                elif second_condition:
                    idx += size2
                else:
                    idx += size3
            if idx == len(sequence_string):
                print(f"FOUND SOLUTION: {size1}, {size2}, {size3}")
                break
        except:
            continue
    print(sequence_string[first_index:first_index + len(first_substring)])
    print(sequence_string[second_index:second_index + len(second_substring)])
    print(sequence_string[third_index:third_index + len(third_substring)])
    abc_sequence = []
    idx = 0
    while idx < len(sequence_string):
        if (sequence_string[idx:idx+size1] == first_substring):
            idx += size1
            abc_sequence.append("A")
        elif (sequence_string[idx:idx+size2] == second_substring):
            idx += size2
            abc_sequence.append("B")
        elif (sequence_string[idx:idx+size3] == third_substring):
            idx += size3
            abc_sequence.append("C")
        else:
            raise NotImplementedError
        print(f"abc_sequence: {abc_sequence}")
        print(f"unconsumed: {sequence_string[idx:]}")
    subsequence_strings = (first_substring, second_substring, third_substring)
    subsequences = (raw_sequence_to_input_string(subsequence_string) for subsequence_string in subsequence_strings)
    abc_sequence = ",".join(abc_sequence)
    print(abc_sequence)
    input_sequence = [abc_sequence]
    for sub in subsequences:
        print(sub)
        input_sequence.append(sub)
    
    input_sequence.append("n\n")
    # input_sequence = [abc_sequence] + [a for a in subsequences] + ["y"]

    input_sequence = "\n".join(input_sequence)

    print(f"Input Sequence as ASCII:\n{input_sequence}")

    input_sequence = input_sequence.encode()

    print(f"Starting program\n")
    icm.feed(program)
    icm.poke(0,2)

    icm.execute()
    input_index = 0
    rowbuffer = []
    while ((status := icm.status()[0]) != 2):
        match status:
            case 3:
                icm.input(input_sequence[input_index])
                input_index += 1
            case 4:
                output = icm.output()
                if output < 255:
                    rowbuffer.append(output)
                    if output == 10:
                        print(bytearray(rowbuffer[:-1]).decode())
                        rowbuffer = []
                else:
                    print(output)


    print(f"Finished program\n")

if __name__ == "__main__":
    main()
