import itertools
import math

INPUT_PATH = "tinput.txt"

def main():
    with open(INPUT_PATH) as f:
        program = [n for n in f.read().strip().split("\n")]

    if INPUT_PATH[0] == "t":
        deck_size = 10
        tracked_cards = [n for n in range(deck_size)]
    else: 
        deck_size = 10007
        tracked_cards = [2019]
    results = [None for _ in range(deck_size)]
    for card in tracked_cards:
        position = card
        # print(f"tracked_card: {card}")
        for instruction in program:
            # print(f"position: {position}")
            print(f"instruction: {instruction}")
            if instruction[:3] == "cut":
                number = int(instruction.split()[-1])
                position = (position - number) % deck_size
            elif instruction[:9] == "deal with":
                number = int(instruction.split()[-1])
                position = (position * number) % deck_size
            elif instruction[:9] == "deal into":
                position = (deck_size - position) % deck_size
        results[position] = card

    print(f"done!")
    print(f"{results}")


if __name__ == "__main__":
    main()
