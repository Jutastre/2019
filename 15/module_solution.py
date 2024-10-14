import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"
WALL = None


class Bfs_node:
    def __sizeof__(self) -> int:
        return len(self.path)

    def __init__(
        self,
        coords: tuple[int, int],
        path: list[str],
        lookup: dict[tuple[int, int] : str | None] = {},
    ) -> None:
        self.coords = coords
        self.lookup = lookup
        self.path = path
        # if (coords in lookup) and len(path) < lookup[coords]:
        #     lookup[coords] = self

        # match path[-1]:
        #     case "n":
        #         self.came_from = "s"
        #     case "s":
        #         self.came_from = "n"
        #     case "w":
        #         self.came_from = "e"
        #     case "e":
        #         self.came_from = "w"


def search(coords, lookup, program):
    path = lookup[coords]
    icm.feed(program)
    icm.execute()
    # icm.output()
    for direction in path:  # travel to this node
        match direction:
            case "n":
                icm.input(1)
            case "s":
                icm.input(2)
            case "w":
                icm.input(3)
            case "e":
                icm.input(4)
        icm.output()
    for direction in ["n", "s", "e", "w"]:
        # if direction == self.came_from:
        #     continue
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
        if target_coords in lookup:
            continue
        match direction:
            case "n":
                icm.input(1)
            case "s":
                icm.input(2)
            case "w":
                icm.input(3)
            case "e":
                icm.input(4)
        output = icm.output()
        match output:
            case 0:
                lookup[target_coords] = WALL
            case 1:
                lookup[target_coords] = [*path, direction]
                match direction:  # walk back to this position
                    case "n":
                        icm.input(2)
                    case "s":
                        icm.input(1)
                    case "w":
                        icm.input(4)
                    case "e":
                        icm.input(3)
                icm.output()
            case 2:
                print(f"HIT {target_coords}; distance is {len(path) + 1}")
                return [*path, direction]
    return False


def main():
    with open(INPUT_PATH) as f:
        data = [int(n) for n in f.read().strip().split(",")]
    icm.feed(data)
    icm.execute()
    # screen = [[" " for _ in range(80)] for __ in range(50)]
    # x = 40
    # y = 25
    # recieved_code = 0

    # first_node = Bfs_node((0,0), [])
    # icm.set_debug(1)
    lookup = {(0, 0): []}
    to_search = [(0, 0)]
    already_searched = []
    depth = 0
    path_to_oxygen = None
    while True:
        depth += 1
        print(f"searching depth {depth}...")
        to_search = []
        for coords in lookup.keys():
            if coords not in already_searched:
                if lookup[coords] == WALL:
                    already_searched.append(coords)
                else:
                    to_search.append(coords)
        print(f"{len(already_searched)} nodes searched before...")
        print(f"{len(to_search)} nodes to process...")
        for coords in to_search:
            if search(coords, lookup, data):
                quit()
            already_searched.append(coords)


if __name__ == "__main__":
    main()
