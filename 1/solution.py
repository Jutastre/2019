INPUT_PATH = "input.txt"

def calc_fuel(mass):
    return max(((int(mass) // 3) - 2), 0)

def main():
    file = open(INPUT_PATH)
    data = file.read().split("\n")

    sum = 0
    for line in data:
        if line:
            module_sum = 0
            fuel_part = int(line)
            while calc_fuel(fuel_part):
                module_sum += calc_fuel(fuel_part)
                fuel_part = calc_fuel(fuel_part)
            sum += module_sum
    
    print(sum)

if __name__ == "__main__":
    main()