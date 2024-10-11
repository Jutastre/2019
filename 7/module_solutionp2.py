import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    icm.set_debug(0)

    best_combination = 0
    best_signal = 0
    # icm.select_machine(-3)
    # combinations = [combination for combination in itertools.permutations(range(5),5)]
    # print(f"all: {combinations}")
    for combination in itertools.permutations(range(5,10),5):
        print(f"Testing combination: {combination}")
        for machine_id in range(5):
            print(f"Initializing machine #{machine_id}")
            icm.select_machine(machine_id)
            print(f"Feeding program to machine #{machine_id}")
            icm.feed(data)
            icm.execute()
            icm.input(combination[machine_id])
            # icm.execute()
            print(f"Finished init; status: {icm.status()}")
        signal = 0
        while (icm.status()[1] != "STATUS_HALTED"):
            for machine_id in range(5):
                print(f"Feeding machine #{machine_id} with signal {signal}")
                icm.select_machine(machine_id)
                icm.input(signal)
                # icm.execute()
                signal = icm.output()
                # icm.execute()
                print(f"machine #{machine_id} returned signal {signal}, status now: {icm.status()[1]}")

        if signal > best_signal:
            best_signal = signal
            best_combination = combination


    print(f"answer:{best_signal}")
    print(f"from combination:{best_combination}")



if __name__ == "__main__":
    main()