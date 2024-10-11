import itertools

INPUT_PATH = "input.txt"



def main():
    file = open(INPUT_PATH)
    data = file.read().strip().split("\n")
    orbits = {}
    for row in data:
        left,right = row.split(")")
        orbits[right] = left
    

    santa_path = []
    body = orbits["SAN"]
    santa_path.append(body)
    while body in orbits:
        body = orbits[body]
        santa_path.append(body)

    body = orbits["YOU"]
    distance = 0
    while body in orbits:
        distance += 1
        body = orbits[body]
        if body in santa_path:
            print(distance)
            print(santa_path.index(body))
            print(distance + santa_path.index(body))
            return


if __name__ == "__main__":
    main()