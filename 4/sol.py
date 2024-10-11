sum = 0

for password in range(387638, 919123):
    string = str(password)
    has_double = False
    has_decreasing = False
    for idx in range(5):
        if int(string[idx]) == int(string[idx + 1]):
            has_double = True
        if int(string[idx]) > int(string[idx + 1]):
            has_decreasing = True
    if has_double and not has_decreasing:
        sum += 1

print(sum)