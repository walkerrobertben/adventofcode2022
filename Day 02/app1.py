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

lines = None
with open("Day 02\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


encryptionReference = {
    "A": "R",
    "B": "P",
    "C": "S",
    "X": "R",
    "Y": "P",
    "Z": "S",
}

totalScore = 0

for line in lines:
    choices = line.split(" ")

    myChoice = encryptionReference[choices[1]]
    theirChoice = encryptionReference[choices[0]]

    myScore = gameScore(myChoice, theirChoice)
    totalScore += myScore

print(totalScore)