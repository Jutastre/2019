import itertools
import math
import time
# import intcodemachine as icm

INPUT_PATH = "input.txt"


def main():
    with open(INPUT_PATH) as f:
        data = [row for row in f.read().strip().split("\n")]


    recipes = []
    for row in data:
        p1,p2 = row.split(" => ")
        result_quantity, result_chem = p2.split(" ")
        result_quantity = int(result_quantity)
        # print(p1)
        # print(p1.split(", "))
        # print([part for part in p1.split(", ")])
        split_sources = [part for part in p1.split(", ")]
        sources = []
        for source_string in split_sources:
            required_quantity,chem = source_string.split(" ")
            required_quantity = int(required_quantity)
            sources.append((required_quantity,chem))
        recipes.append((sources,(result_quantity, result_chem)))

    print(recipes)

    recipe_dict = {}
    for rec in recipes:
        chem = rec[1][1]
        required_quantity = rec[1][0]
        sources = rec[0]
        recipe_dict[chem] = (required_quantity,sources)

    requirements = {"FUEL":1}
    leftovers = {}
    while not (len([a for a in requirements.keys()]) == 1 and [a for a in requirements.keys()][0] == "ORE"):
        new_requirements = {}
        new_requirements = {}
        for chem,required_quantity in requirements.items():
            if chem == 'ORE': # ORE is just passed on to next generation as is
                if chem in new_requirements:
                    new_requirements[chem] += required_quantity
                else:
                    new_requirements[chem] = required_quantity
                continue

            if chem in leftovers: # take from leftovers first if there are any
                leftover_quantity = leftovers.pop(chem)
                required_quantity -= leftover_quantity
                if required_quantity < 0:
                    leftovers[chem] = 0 - required_quantity # stow remainder in leftovers
            while required_quantity > 0: # lastly, produce more

                for source_quantity,source_chem in recipe_dict[chem][1]:
                    if source_chem in new_requirements:
                        new_requirements[source_chem] += source_quantity
                    else:
                        new_requirements[source_chem] = source_quantity
                required_quantity -= recipe_dict[chem][0]
                if required_quantity < 0:
                    leftovers[chem] = 0 - required_quantity # stow remainder in leftovers
        requirements = new_requirements
        # print(f"-------------------")
        # print(f"requirements: {requirements}")
        # print(f"leftovers: {leftovers}")
        # time.sleep(0.5)

    print(f"answer: {list(requirements.values())[0]}")



if __name__ == "__main__":
    main()