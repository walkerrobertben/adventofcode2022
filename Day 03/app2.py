
def priority(item):
    v = ord(item)
    if (v >= 65 and v <= 90):
        return v - 65 + 27
    elif (v >= 97 and v <= 122):
        return v - 97 + 1

def findCommon(b1, b2, b3):
    for item in b1:
        if b2.find(item) != -1:
            if b3.find(item) != -1:
                return item


lines = None
with open("Day 03\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

i = 0
total = 0

while (i < len(lines)):

    b1 = lines[i]
    b2 = lines[i + 1]
    b3 = lines[i + 2]

    item = findCommon(b1, b2, b3)
    total += priority(item)
    i += 3

print(total)