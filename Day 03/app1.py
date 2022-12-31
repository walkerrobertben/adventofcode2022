
def priority(item):
    v = ord(item)
    if (v >= 65 and v <= 90):
        return v - 65 + 27
    elif (v >= 97 and v <= 122):
        return v - 97 + 1

def findDuplicate(c1, c2):
    for item in c1:
        if c2.find(item) != -1:
            return item


lines = None
with open("Day 3\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

total = 0

for line in lines:
    c1 = line[:int(len(line)/2)]
    c2 = line[int(len(line)/2):]

    item = findDuplicate(c1, c2)
    total += priority(item)

print(total)