lines = None
with open("Day 6\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


for line in lines:

    for i in range(0, len(line)):

        found = {}
        fourChars = line[i:i+4]

        for c in fourChars:
            if c in found:
                break
            else:
                found[c] = True

        if len(found.keys()) == 4:
            print(i+4)
            break
