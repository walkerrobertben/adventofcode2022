def gameScore(myChoice, theirChoice):
    
    choiceScore = (myChoice == "R" and 1) or (myChoice == "P" and 2) or (myChoice == "S" and 3)
    resultScore = 0

    if myChoice == "R":
        if theirChoice == "R":
            resultScore = 3
        elif theirChoice == "P":
            resultScore = 0
        elif theirChoice == "S":
            resultScore = 6
    elif myChoice == "P":
        if theirChoice == "R":
            resultScore = 6
        elif theirChoice == "P":
            resultScore = 3
        elif theirChoice == "S":
            resultScore = 0
    elif myChoice == "S":
        if theirChoice == "R":
            resultScore = 0
        elif theirChoice == "P":
            resultScore = 6
        elif theirChoice == "S":
            resultScore = 3

    return resultScore + choiceScore



def calculateChoice(theirChoice, desiredOutcome):
    if theirChoice == "R":
        if desiredOutcome == "W":
            return "P"
        elif desiredOutcome == "D":
            return "R"
        elif desiredOutcome == "L":
            return "S"
    elif theirChoice == "P":
        if desiredOutcome == "W":
            return "S"
        elif desiredOutcome == "D":
            return "P"
        elif desiredOutcome == "L":
            return "R"
    elif theirChoice == "S":
        if desiredOutcome == "W":
            return "R"
        elif desiredOutcome == "D":
            return "S"
        elif desiredOutcome == "L":
            return "P"



lines = None
with open("Day 02\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


encryptionReference = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "L",
    "Y": "D",
    "Z": "W",
}

totalScore = 0

for line in lines:
    choices = line.split(" ")

    theirChoice = encryptionReference[choices[0]]
    desiredOutcome = encryptionReference[choices[1]]

    #myChoice = encryptionReference[choices[1]]
    myChoice = calculateChoice(theirChoice, desiredOutcome)

    myScore = gameScore(myChoice, theirChoice)
    totalScore += myScore

print(totalScore)