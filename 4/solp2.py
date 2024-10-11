sum = 0

for password in range(387638, 919123):
    string = str(password)
    has_double_without_neighbours = False
    has_decreasing = False
    for idx in range(5):
        if int(string[idx]) == int(string[idx + 1]):
            if (idx == 0):
                if (string[idx+2] != string[idx]):
                    has_double_without_neighbours = True
            elif (idx == 4):
                if (string[idx-1] != string[idx]):
                    has_double_without_neighbours = True
            elif (string[idx+2] != string[idx]) and (string[idx-1] != string[idx]):
                has_double_without_neighbours = True
        if int(string[idx]) > int(string[idx + 1]):
            has_decreasing = True
    if has_double_without_neighbours and not has_decreasing:
        sum += 1
        print(password)

print(sum)