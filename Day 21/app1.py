lines = None
with open("Day 21\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

monkeys = {}

class Monkey:
    def __init__(self, name, data):
        if data.isnumeric():
            self.value = int(data)

        else:
            m1, op, m2 = data.split(" ")

            def calculate():
                n1 = monkeys[m1].getNumber()
                n2 = monkeys[m2].getNumber()
                if op == "+":
                    return n1 + n2
                elif op == "-":
                    return n1 - n2
                elif op == "*":
                    return n1 * n2
                elif op == "/":
                    return n1 / n2

            self.getNumber = calculate

    def getNumber(self):
        return self.value
            

for line in lines:
    name, job = line.split(": ")
    monkeys[name] = Monkey(name, job)
    
print(monkeys["root"].getNumber())