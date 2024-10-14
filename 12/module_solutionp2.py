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
    periods = [None,None,None]
    for axis in range(3):
        previous = set()
        step = 0
        while True:
            for moon1, moon2 in itertools.combinations(moons, 2):
                if moon1[0][axis] < moon2[0][axis]:
                    moon1[1][axis] += 1
                    moon2[1][axis] -= 1
                elif moon1[0][axis] > moon2[0][axis]:
                    moon1[1][axis] -= 1
                    moon2[1][axis] += 1
            for moon in moons:
                moon[0][axis] += moon[1][axis]
            
            hash = (moons[0][0][axis],moons[0][1][axis],moons[1][0][axis],moons[1][1][axis],moons[2][0][axis],moons[2][1][axis],moons[3][0][axis],moons[3][1][axis])
            if hash in previous:
                periods[axis] = step
                break
            previous.add(hash)
            step += 1 #why is this not at the start of the calculation?
    lcm = math.lcm(periods[0],periods[1],periods[2])
    print(lcm)





if __name__ == "__main__":
    main()