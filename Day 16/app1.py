lines = None
with open("Day 16\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]
    
class Node:
    def __init__(self, rate, edges):
        self.rate = rate
        self.edges = edges

class Edge:
    def __init__(self, to):
        self.to = to
        self.cost = 1

#build graph
graph = {}
for line in lines:
    this, edges = line.split("; ")
    node, rate = this.split(" has ")

    nodeKey = node[6:]
    nodeRate = int(rate[rate.find("rate=")+5:])

    nodeEdges = []
    edgeKeys = edges.strip("tunnel leads to valve ").strip("tunnels lead to valves ").split(", ")
    for edgeKey in edgeKeys:
        nodeEdges.append(Edge(edgeKey))

    graph[nodeKey] = Node(nodeRate, nodeEdges)

#make f cached
def cache(f):
    memory = {}
    def cached(*args):
        if not args in memory:
            memory[args] = f(*args)
        return memory[args]
    return cached

#bfs between nodes to find shortest path
@cache
def path(keyFrom, keyTo):

    if keyFrom == keyTo:
        return [keyFrom]

    routes = [[keyFrom]]
    visited = set()

    while len(routes) > 0:

        route = routes.pop(0)
        this = route[-1]

        if not this in visited:
            visited.add(this)

            for edge in graph[this].edges:
                if not edge.to in visited:

                    new_route = route.copy()
                    new_route.append(edge.to)

                    if edge.to == keyTo:
                        return new_route

                    routes.append(new_route)
    return None

nodesToVisit = []
for key, node in graph.items():
    if node.rate > 0:
        nodesToVisit.append(key)

startKey = "AA"
timeLimit = 30
best_pressure = 0

branches = [[startKey, 0, {}]]

while len(branches) > 0:

    [currentKey, minutesSimulated, openedValves] = branches.pop()

    if minutesSimulated >= timeLimit or len(openedValves) == len(nodesToVisit):

        #calculate pressure released
        pressure = 0
        for key, openedAt in openedValves.items(): 
            minutesOpened = max(timeLimit - openedAt, 0)
            pressure += graph[key].rate * minutesOpened

        best_pressure = max(best_pressure, pressure)

    else:

        #for every node we should visit
        for destinationKey in nodesToVisit:

            #if we haven't opened that node on this route already
            if not destinationKey in openedValves:

                #if there is a path to that node
                keyPath = path(currentKey, destinationKey)
                if keyPath != None:

                    #write this to branches
                    new_currentKey = destinationKey
                    new_minutesSimulated = minutesSimulated + (len(keyPath) - 1) + (1) #time to walk + time to open
                    new_openedValves = openedValves.copy()
                    new_openedValves[destinationKey] = new_minutesSimulated

                    branches.append([new_currentKey, new_minutesSimulated, new_openedValves])

print(best_pressure)