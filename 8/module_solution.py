import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        # data = [[row[9:] for row in number.split("\n")] for number in f.read().strip().split("\n\n")]
        data = f.read().strip()
        # data = [[data[start:start+25] for start in range(layer_start, layer_start + 25*6, 25)] for layer_start in range(0, len(data), 25*6)]
        data = [data[layer_start:layer_start+25 * 6] for layer_start in range(0, len(data), 25*6)]

    print(f"data:{data}")
    minimum = None
    min_index = None

    for index, layer in enumerate(data):
        # count = "".join(layer).count(0)
        count = layer.count("0")
        if minimum == None:
            minimum = count
            min_index = index
        if (count < minimum):
            minimum = count
            min_index = index

    # data[min_index].count("1") * data[min_index].count("2")

    print(f"answer:{data[min_index].count("1") * data[min_index].count("2")}")



if __name__ == "__main__":
    main()