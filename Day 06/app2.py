lines = None
with open("Day 06\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


def findMarker(string, start, n):
    for i in range(start, len(string)):

        found = {}
        for c in string[i:i+n]:
            if c in found:
                break
            else:
                found[c] = True

        if len(found.keys()) == n:
            return i+n


for line in lines:

    startOfPacket = findMarker(line, 0, 4)
    startOfMessage = findMarker(line, startOfPacket, 14)
    print(startOfMessage)
