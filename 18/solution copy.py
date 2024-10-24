import itertools
import math


INPUT_PATH = "tinput.txt"

def find_all_pois(map:list[str]):
    found_pois = {}
    for y,row in enumerate(map):
        for x,char in enumerate(row):
            if char.isalpha():
                found_pois[char] = (x,y)
            if char == "@":
                found_pois[char] = (x,y)
    return found_pois

# def find_keys(coords:tuple[int,int], keyset:set, map, memo = {}):
#     hashen = hash((coords, tuple(keyset)))
#     if hashen not in memo:
#         found_keys = []

#         history = set()
#         to_search_next = [coords]

#         while to_search_next:
#             to_search = [coord for coord in to_search_next]
#             to_search_next = []
#             for coordinates in to_search:
#                 history.add(coordinates)
#                 for direction in ["n", "s", "e", "w"]:
#                     x,y = coordinates
#                     match direction:
#                         case "n":
#                             target_coords = (x, y - 1)
#                         case "s":
#                             target_coords = (x, y + 1)
#                         case "w":
#                             target_coords = (x - 1, y)
#                         case "e":
#                             target_coords = (x + 1, y)
#                     if target_coords in history:
#                         continue
#                     tx,ty = target_coords
#                     output:str = map[ty][tx]
#                     match output:
#                         case "#":
#                             continue
#                         case ".":
#                             to_search_next.append(target_coords)
#                         case _:
#                             if output in keyset:
#                                 to_search_next.append(target_coords)
#                             elif output.islower():
#                                 to_search_next.append(target_coords)
#                                 found_keys.append(output)
#                             elif output.lower() in keyset:
#                                 to_search_next.append(target_coords)
#         memo[hashen] = set(found_keys)
#     return memo[hashen]

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
    return results



def path_is_shorter_alternative(path:tuple[list[str], int], alternative:tuple[list[str], int]):
    if path[0][-1] == alternative[0][-1] and path[1] >= alternative[1]:
        if set(path[0]) == set(alternative[0]):
            return True
    return False

def path_has_all_keys(path, keys:set):
    return set(path).issuperset(keys)

def main():
    with open(INPUT_PATH) as f:
        map:list[str] = [row for row in f.read().strip().split("\n")]

    keymap = []

    for x,y in itertools.product(range(len(map[0])), range(len(map))):
        if map[y][x] == "@":
            start_position = (x,y)
            #map[y] = map[y].replace("@", ".")
            break

    all_keys = find_all_pois(map)
    print(all_keys["@"])

    distances = {key:find_distances(coord,map) for key,coord in all_keys.items()}
    print(distances["@"])

    keys = set([key for key in all_keys.keys() if key.islower()])

    print(keys)
    paths = [([key],distance) for key,distance in distances["@"].items()]
    print(paths)
    finished = False
    finished_paths = []
    while not finished: # dirty way to iterate len(keys) - 1
        new_paths = []
        for path,distance in paths:
            if path_has_all_keys(path,keys):
                finished_paths.append((path,distance))
                continue
            new_options = [(key,distance) for key,distance in distances[path[-1]].items()] # if key not in path
            for option in new_options:
                if option[0].isupper() and option[0].lower() not in path:
                    continue
                new_path = ([key for key in path], distance)
                new_path[0].append(option[0])
                new_path = (new_path[0], new_path[1] + option[1])
                new_index = -1
                for idx,already_found in enumerate(new_paths):
                    if path_is_shorter_alternative(already_found, new_path):
                        new_index = idx
                        break
                if new_index == -1:
                    new_paths.append(new_path)
                else:
                    new_paths[new_index] = new_path
        paths = new_paths

        finished = True
        for path_distance, key in itertools.product(paths, keys):
            if key not in path_distance[0]:
                finished = False
                break
        print(f"working with {len(paths)}")
        print(f"finished: {len(finished_paths)}")
    print(paths)

    # shortest_so_far = None
    # for key_order in possible_orders:
    #     keyset = set()
    #     current_coordinates = start_position
    #     distance_accumulator = 0
    #     for key in key_order:
    #         span_distance, new_position = find_distance(current_coordinates, keyset, map, key)
    #         distance_accumulator += span_distance
    #         current_coordinates = new_position
    #         keyset.add(key)
    #     if not shortest_so_far or distance_accumulator < shortest_so_far[1]:
    #         shortest_so_far = (key_order, distance_accumulator)

    # print(f"shortest: {shortest_so_far}")

if __name__ == "__main__":
    main()
