import itertools
import math
import intcodemachine as icm

INPUT_PATH = "input.txt"

def calculate_energy(moon):
    return sum(abs(n) for n in moon[0]) * sum(abs(n) for n in moon[1])

def main():
    with open(INPUT_PATH) as f:
        data = [row for row in f.read().strip().split("\n")]
    moons = []

    for scan in data:
        position = [int(axis[2:]) for axis in scan.strip("<>").split(", ")]
        velocity = [0,0,0]
        moons.append((position,velocity))
    
    for _ in range(1000):
        for moon1, moon2 in itertools.combinations(moons, 2):
            for axis in range(3):
                if moon1[0][axis] < moon2[0][axis]:
                    moon1[1][axis] += 1
                    moon2[1][axis] -= 1
                elif moon1[0][axis] > moon2[0][axis]:
                    moon1[1][axis] -= 1
                    moon2[1][axis] += 1
        for moon in moons:
            for axis in range(3):
                moon[0][axis] += moon[1][axis]
    print(moons)


    print(f"answer: {sum(calculate_energy(moon) for moon in moons)}")



if __name__ == "__main__":
    main()