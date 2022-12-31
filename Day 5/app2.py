lines = None
with open("Day 5\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

stacks = []

readingItems = True
readStackCount = False
hasReversedStacks = False

def moveItems(count, fromStack, toStack):
    n = len(stacks[fromStack-1]) - count

    items = stacks[fromStack-1][n:]
    for item in items:
        stacks[toStack-1].append(item)

    stacks[fromStack-1] = stacks[fromStack-1][:n]


for line in lines:
    if line != "":

        if line[0] == " " and line[1] == "1":
            readingItems = False

        if readingItems:
            if readStackCount == False:
                stackCount = int((len(line) + 1) / 4)
                readStackCount = True
                
                for i in range(0, stackCount):
                    stacks.append([])

            i = 0
            n = 0
            while (i < len(line)):
                item = line[i+1:i+2]
                if item != " ":
                    stacks[n].append(item)

                i += 4
                n += 1
        else:

            if hasReversedStacks == False:
                for stack in stacks:
                    stack.reverse()

                hasReversedStacks = True

            if line[0:4] == "move":

                line = line[5:]
                i1 = line.find(" from ")
                i2 = line.find(" to ")

                count = int(line[:i1])
                fromStack = int(line[i1 + 6 : i2])
                toStack = int(line[i2 + 4])

                moveItems(count, fromStack, toStack)


result = ""
for stack in stacks:
    result += stack.pop()

print(result)