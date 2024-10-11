import itertools
import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    # intcodemachine.set_debug(True)
    with open(INPUT_PATH) as f:
        # data = [[row[9:] for row in number.split("\n")] for number in f.read().strip().split("\n\n")]
        data = f.read().strip()
        data = [[data[start:start+25] for start in range(layer_start, layer_start + 25*6, 25)] for layer_start in range(0, len(data), 25*6)]
        # data = [data[layer_start:layer_start+25 * 6] for layer_start in range(0, len(data), 25*6)]

    print(f"data:{data}")

    canvas = [''.join(['2' for _ in range(25)]) for __ in range(6)]

    for layer in data:
        for col in range(25):
            for row in range(6):
                if canvas[row][col] == "2":
                    canvas[row] = canvas[row][:col] + layer[row][col] + canvas[row][col+1:]


    # data[min_index].count("1") * data[min_index].count("2")

    print(f"answer:\n{"\n".join(canvas)}")



if __name__ == "__main__":
    main()