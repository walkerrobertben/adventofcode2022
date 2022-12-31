lines = None
with open("Day 09\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

rn = 10

rope = []
for i in range(0, rn):
    rope.append([0,0])

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

        rope[0][0] += dir[0]
        rope[0][1] += dir[1]

        for j in range(0, rn-1):

            r0 = rope[j]
            r1 = rope[j+1]

            dX = r0[0] - r1[0]
            dY = r0[1] - r1[1]
            d2 = dX * dX + dY * dY

            #check moved side to side
            if dX != 0:
                if d2 >= 2*2:
                    r1[0] += (dX >= 0 and 1 or -1)

            #check moved up or down
            if dY != 0:
                if d2 >= 2*2:
                    r1[1] += (dY >= 0 and 1 or -1)

        tpos = str(rope[rn-1])
        visited[tpos] = True

print(len(visited.keys()))