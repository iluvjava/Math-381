modified = ""
with open("All Meals.txt", 'r') as f:
    lines = f.readlines()
    modified += lines[0]
    for line in lines[1:]:
        occurence = 3
        for letter, I in zip(line, range(len(line))):
            if letter == ',':
                occurence -= 1
            if occurence == 0:
                modified += line[:I] + "400" + line[I:]
                break

print(modified)
