import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"

INPUT_VALUE = 5
DEBUG_LEVEL = 0

def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    icm.set_debug(DEBUG_LEVEL)

    output_data = []

    icm.feed(data)
    icm.execute()
    while icm.status()[1] != "STATUS_HALTED":
        print(icm.status())
        match icm.status()[1]:
            case "STATUS_AWAITING_INPUT":
                icm.input(INPUT_VALUE)
            case "STATUS_AWAITING_OUTPUT":
                output_data.append(icm.output())
                print(f"read {output_data[-1]} from icm")
        icm.execute()
    

    # output = icm.read()

    print(f"answer:{output_data}")



if __name__ == "__main__":
    main()