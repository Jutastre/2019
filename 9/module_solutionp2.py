import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [int(number) for number in f.read().strip().split(",")]

    # icm.set_debug(1)

    icm.feed(data)
    icm.execute()
    icm.input(2)
    # icm.execute()
    while icm.status()[0] == 4:
        print(icm.output())
        # icm.execute()
        
    # output = icm.output()


    # print(f"answer:{output}")



if __name__ == "__main__":
    main()