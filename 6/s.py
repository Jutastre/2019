import itertools

INPUT_PATH = "input.txt"



def main():
    file = open(INPUT_PATH)
    data = file.read().strip().split("\n")
    orbits = {}
    sum = 0
    for row in data:
        left,right = row.split(")")
        orbits[right] = left
    
    bodies = [body for body in set(orbits.keys()).union(set(orbits.values()))]
    for body in bodies:
        while body in orbits:
            sum += 1
            body = orbits[body]
    print(sum)


if __name__ == "__main__":
    main()