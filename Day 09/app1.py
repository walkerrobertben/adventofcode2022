lines = None
with open("Day 09\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


tail = [0,0]
head = [0,0]

visited = {}

dirs = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0)
}

for line in lines:
    [dirString, stepsString] = line.split(" ")
    dir = dirs[dirString]
    steps = int(stepsString)

    for i in range(0, steps):
        head[0] += dir[0]
        head[1] += dir[1]

        moveX = head[0] != tail[0]
        moveY = head[1] != tail[1]

        dX = head[0] - tail[0]
        dY = head[1] - tail[1]
        d2 = dX * dX + dY * dY

        #check moved side to side
        if moveX:
            d = head[0] - tail[0]
            if d2 >= 2*2:
                tail[0] += (d >= 0 and 1 or -1)

        #check moved up or down
        if moveY:
            d = head[1] - tail[1]
            if d2 >= 2*2:
                tail[1] += (d >= 0 and 1 or -1)

        tpos = str(tail)

        visited[tpos] = True

print(len(visited.keys()))