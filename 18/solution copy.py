import itertools
import math


INPUT_PATH = "tinput.txt"

def find_all_pois(map:list[str]):
    found_pois = {}
    for y,row in enumerate(map):
        for x,char in enumerate(row):
            if char.islower():
                found_pois[char] = (x,y)
    return found_pois

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

def find_distances(coords, map):
    distance = 0
    results = {}

    history = set()
    to_search_next = [coords]

    while to_search_next:
        distance += 1
        to_search = to_search_next
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
                        results[output] = distance
    raise ValueError("WTF")





def main():
    with open(INPUT_PATH) as f:
        map:list[str] = [row for row in f.read().strip().split("\n")]

    keymap = []

    for x,y in itertools.product(range(len(map[0])), range(len(map))):
        if map[y][x] == "@":
            start_position = (x,y)
            map[y] = map[y].replace("@", ".")
            break

    all_keys = find_all_pois(map)

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
