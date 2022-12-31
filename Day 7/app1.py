lines = None
with open("Day 7\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


class File:
    size = 0
    def __init__(self, size):
        self.size = size

class Directory:

    name = None
    parentDirectory = None

    files = None # []
    subDirectories = None # []

    def __init__(self, name):
        self.name = name
        self.files = []
        self.subDirectories = []
    
    def setParentDirectory(self, parentDirectory):
        self.parentDirectory = parentDirectory

    def addFile(self, file):
        self.files.append(file)

    def addSubdirectory(self, subDirectory):
        subDirectory.setParentDirectory(self)
        self.subDirectories.append(subDirectory)

    def getSubdirectory(self, subDirectoryName):
        for subDirectory in self.subDirectories:
            if subDirectory.name == subDirectoryName:
                return subDirectory

    def getSubdirectories(self):
        return self.subDirectories

    def computeSize(self):
        sum = 0

        for file in self.files:
            sum += file.size

        for subDirectory in self.subDirectories:
            sum += subDirectory.computeSize()

        return sum

root = Directory("root")

cwd = None
cmd = None

for line in lines:
    if line[0] == "$":
        #new command

        commandParts = line[2:].split(" ")
        command = commandParts[0]
        parameter = len(commandParts) == 2 and commandParts[1] or None

        cmd = command

        if command == "cd":
            if parameter == "/":
                cwd = root
            elif parameter == "..":
                cwd = cwd.parentDirectory
            else:
                cwd = cwd.getSubdirectory(parameter)

        elif command == "ls":
            pass

    else:
        if cmd == "ls":

            lsParts = line.split(" ")
 
            if lsParts[0] == "dir": #its a directory
                _, subDirectoryName = lsParts[0], lsParts[1]
                subDirectory = Directory(subDirectoryName)
                cwd.addSubdirectory(subDirectory)
                
            else: #its a file
                fileSize, fileName = lsParts[0], lsParts[1]
                file = File(int(fileSize))
                cwd.addFile(file)

#print(root.computeSize())

sum = 0

def scanDirectory(directory):
    global sum

    size = directory.computeSize()

    print(directory.name, size)

    if size <= 100000:
        sum += size

    for subDirectory in directory.getSubdirectories():
        scanDirectory(subDirectory)

scanDirectory(root)
print(sum)