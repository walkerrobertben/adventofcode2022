lines = None
with open("Day 10\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

cycle = 1
registers = {
    "x": 1
}

history = {} #after cycle n, register value is..

def capture(): 
    for register, value in registers.items():
        if not register in history:
            history[register] = {}
        history[register][cycle] = value

capture()


# noop: 1 cycle
# addx: 1 cycle, increment, 1 cycle



#run program
for line in lines:

    iparts = line.split(" ")
    instruction = iparts[0]

    if instruction == "noop":
        #instruction step 1 done
        cycle += 1

    elif instruction == "addx":
        #instruction step 1 done
        cycle += 1

        registers["x"] += int(iparts[1])
        capture()

        #instruction step 2 done
        cycle += 1
        

#fill gaps
for register, values in history.items():
    v = None
    for i in range(1, cycle):
        if i in values:
            v = values[i]
        else:
            values[i] = v

#calculate
total = 0

for i in range(20, cycle, 40):
    x = history["x"][i-1] #during cycle i, value is that of cycle[i-1]
    total += i * x

print(total)