import itertools
import math


INPUT_PATH = "tinput.txt"

def find_all_keys(map:list[str]):
    found_keys = set()
    for row in map:
        for char in row:
            if char.islower():
                found_keys.add(char)
    return found_keys

def find_keys(coords:tuple[int,int], keyset:set, map, memo = {}):
    hashen = hash((coords, tuple(keyset)))
    if hashen not in memo:
        found_keys = []

        history = set()
        to_search_next = [coords]

        while to_search_next:
            to_search = [coord for coord in to_search_next]
            to_search_next = []
            for coordinates in to_search:
                history.add(coordinates)
                for direction in ["n", "s", "e", "w"]:
                    x,y = coordinates
                    match direction:
                        case "n":
                            target_coords = (x, y - 1)
                        case "s":
                            target_coords = (x, y + 1)
                        case "w":
                            target_coords = (x - 1, y)
                        case "e":
                            target_coords = (x + 1, y)
                    if target_coords in history:
                        continue
                    tx,ty = target_coords
                    output:str = map[ty][tx]
                    match output:
                        case "#":
                            continue
                        case ".":
                            to_search_next.append(target_coords)
                        case _:
                            if output in keyset:
                                to_search_next.append(target_coords)
                            elif output.islower():
                                to_search_next.append(target_coords)
                                found_keys.append(output)
                            elif output.lower() in keyset:
                                to_search_next.append(target_coords)
        memo[hashen] = set(found_keys)
    return memo[hashen]

def find_distance(coords, keyset, map, goal):
    distance = 0

    history = set()
    to_search_next = [coords]

    while to_search_next:
        distance += 1
        to_search = [coord for coord in to_search_next]
        to_search_next = []
        for coordinates in to_search:
            history.add(coordinates)
            for direction in ["n", "s", "e", "w"]:
                x,y = coordinates
                match direction:
                    case "n":
                        target_coords = (x, y - 1)
                    case "s":
                        target_coords = (x, y + 1)
                    case "w":
                        target_coords = (x - 1, y)
                    case "e":
                        target_coords = (x + 1, y)
                if target_coords in history:
                    continue
                tx,ty = target_coords
                output:str = map[ty][tx]
                match output:
                    case "#":
                        continue
                    case ".":
                        to_search_next.append(target_coords)
                    case _:
                        if output == goal:
                            return (distance, target_coords)
                        elif (output in keyset) or (output.islower()) or (output.lower() in keyset):
                            to_search_next.append(target_coords)
    raise ValueError("WTF")


def get_distance(coords, goal, distance, keyset, map, result, history = None):
    if not history:
        history = set()
    history.add(coords)
    for direction in ["n", "s", "e", "w"]:
        x,y = coords
        match direction:
            case "n":
                target_coords = (x, y - 1)
            case "s":
                target_coords = (x, y + 1)
            case "w":
                target_coords = (x - 1, y)
            case "e":
                target_coords = (x + 1, y)
        if target_coords in history:
            continue
        tx,ty = target_coords
        output = map[ty][tx]
        match output:
            case "#":
                continue
            case ".":
                get_distance(target_coords, goal, distance + 1, keyset, map, result, history)
            case _:
                if output == goal:
                    result = min(distance + 1, result)
                if output in keyset:
                    get_distance(target_coords, goal, distance + 1, keyset, map, result, history)
                else:
                    continue
    return False

def recursive(start_position,obtained_keys:list,all_keys:set, map, memo = {}):
    hashen = hash((start_position,tuple(obtained_keys)))
    if hashen in memo:
        return memo[hashen]
    possibilities = []
    if len(obtained_keys) == len(all_keys):
        memo[hashen] = [obtained_keys]
        return [obtained_keys]
    for next_key in find_keys(start_position, obtained_keys, map):
        obtained_copy = [a for a in obtained_keys] + [next_key]
        result = recursive(start_position,obtained_copy,all_keys, map)
        if result:
            possibilities += result
    memo[hashen] = possibilities
    return possibilities


def main():
    with open(INPUT_PATH) as f:
        map:list[str] = [row for row in f.read().strip().split("\n")]

    keymap = []

    for x,y in itertools.product(range(len(map[0])), range(len(map))):
        if map[y][x] == "@":
            start_position = (x,y)
            map[y] = map[y].replace("@", ".")
            break

    all_keys = find_all_keys(map)

    # found_keys = set()

    possible_orders = recursive(start_position,[],all_keys,map)
    # possible_orders = []
    # count = 0
    # fake_count = 0
    for p in possible_orders:
        print(p)
    print(f"total possibilities: {len(possible_orders)}")
    print(f"total combinations: {math.factorial(len(all_keys))}")

    # available_first = find_keys(start_position, set(), map)
    # available_second = available_first.union(find_keys(start_position, available_first, map))

    # print(f"available_first: {available_first}")
    # print(f"available_second: {available_second}")

    # for key_order in itertools.permutations(all_keys, len(all_keys)):
    #     # count += 1
    #     # fake_count += 1
    #     if key_order[0] not in available_first:
    #         continue
    #     # if key_order[1] not in available_second:
    #     #     continue
    #     # print(key_order)
    #     obtained_keys = set()
    #     for next_key in key_order:
    #         if next_key not in (dbg:=find_keys(start_position, obtained_keys, map)):
    #             break
    #         obtained_keys.add(next_key)
    #     if obtained_keys == all_keys:
    #         possible_orders.append(key_order)
    #         # print(f"order: {key_order} is possible")
    #     # if count % 100 == 0:
    #     #     print(f"tried {count} combinations...")
    # # print(fake_count)
    shortest_so_far = None
    for key_order in possible_orders:
        keyset = set()
        current_coordinates = start_position
        distance_accumulator = 0
        for key in key_order:
            span_distance, new_position = find_distance(current_coordinates, keyset, map, key)
            distance_accumulator += span_distance
            current_coordinates = new_position
            keyset.add(key)
        if not shortest_so_far or distance_accumulator < shortest_so_far[1]:
            shortest_so_far = (key_order, distance_accumulator)

    print(f"shortest: {shortest_so_far}")

if __name__ == "__main__":
    main()
