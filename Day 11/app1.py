import math

lines = None
with open("Day 11\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

def add(a,b):
    return a+b
def multiply(a,b):
    return a*b

operators = {
    "+": add,
    "*": multiply
}

def readMonkey(n):

    monkey = int(lines[n][7:].strip(":"))

    startingItems = list(map(int, lines[n+1][18:].split(", ")))

    operation = lines[n+2][19:]
    def operationMethod(old):
        term1 = old
        operator = operators[operation[4]]
        term2 = operation[6:]
        term2 = term2 == "old" and old or int(term2)
        return operator(term1, term2)

    divisible = int(lines[n+3][20:])
    def divisibleMethod(value):
        return value % divisible == 0

    testTrue = int(lines[n+4][29:])
    testFalse = int(lines[n+5][30:])

    return {
        "monkey": monkey,
        "items": startingItems,
        "operation": operationMethod,
        "test": divisibleMethod,
        "throwIfTrue": testTrue,
        "throwIfFalse": testFalse,
        "inspects": 0,
    }


monkeys = {}

for i, line in enumerate(lines):
    if line[0:6] == "Monkey": #reading new monkey
        monkey = readMonkey(i)
        monkeys[monkey["monkey"]] = monkey

def printItems():
    for n, monkey in monkeys.items():
        print(n, monkey["items"])

for round in range(0, 20):
    print("Round", round+1)
    for n, monkey in monkeys.items():
        
        #inspect items
        #apply operation to item
        #worry level divided by 3
        #monkey test is performed on item
        #item thrown to other monkey

        monkey["items"].reverse()

        while len(monkey["items"]) > 0:

            monkey["inspects"] += 1
            item = monkey["items"].pop()

            item = monkey["operation"](item)
            item = math.floor(item / 3)
            
            target = monkey["throwIfFalse"]
            if monkey["test"](item):
                target = monkey["throwIfTrue"]

            monkeys[target]["items"].append(item)

inspects = []
for n, monkey in monkeys.items():
    inspects.append(monkey["inspects"])
inspects.sort(reverse=True)

print(inspects)
print(inspects[0] * inspects[1])