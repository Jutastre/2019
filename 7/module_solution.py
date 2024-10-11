import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    icm.set_debug_global(2)

    best_combination = 0
    best_signal = 0
    # icm.select_machine(-3)
    # combinations = [combination for combination in itertools.permutations(range(5),5)]
    # print(f"all: {combinations}")
    for combination in itertools.permutations(range(5),5):
        print(f"Testing combination: {combination}")
        for machine_id in range(5):
            print(f"Initializing machine #{machine_id}")
            icm.select_machine(machine_id)
            print(f"Feeding program to machine #{machine_id}")
            icm.feed(data)
            icm.execute()
            print(f"inputting {combination[machine_id]}")
            icm.input(combination[machine_id])
            print(icm.status())
            # icm.execute()
            print(f"Finished init; status: {icm.status()}")
        signal = 0
        for machine_id in range(5):
            print(f"Feeding machine #{machine_id} with signal {signal}")
            icm.select_machine(machine_id)
            icm.input(signal)
            # icm.execute()
            signal = icm.output()
            print(f"machine #{machine_id} returned signal {signal}")

        if signal > best_signal:
            best_signal = signal
            best_combination = combination


    print(f"answer:{best_signal}")
    print(f"from combination:{best_combination}")



if __name__ == "__main__":
    main()