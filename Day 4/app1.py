

#a range is a tuple with 2 values
#2-4 means sections 2, 3, 4
#this is represented by the tuple (2,4)

#test is range2 is contained in range1
def rangeContains(range1, range2):
    if range2[0] >= range1[0]:
        if range2[1] <= range1[1]:
            return True
    return False

def rangeTupleFromString(rangeString):
    [n1, n2] = rangeString.split("-")
    return (int(n1), int(n2))

lines = None
with open("Day 4\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


total = 0

for line in lines:
    [rangeString1, rangeString2] = line.split(",")

    range1 = rangeTupleFromString(rangeString1)
    range2 = rangeTupleFromString(rangeString2)

    if rangeContains(range1, range2) or rangeContains(range2, range1):
        total += 1

print(total)