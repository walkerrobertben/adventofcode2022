#goal: crack most geodes
#geode-crackers
#obsidian-collecting
#clay-collecting
#ore-collecting

import math

lines = None
with open("Day 19\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

sim_limit = 24
robot_types = ("ore", "clay", "obsidian", "geode")

def parse_blueprint(line):
    line = line[line.find(": ")+2:]

    blueprint = {}
    for robot_type in robot_types:
        blueprint[robot_type] = {}

        i1 = line.find(robot_type) + len(robot_type + " robot costs ")
        i2 = line.find(".", i1)
        costs = line[i1:i2].split(" and ")

        for cost in costs:
            [amount, resource] = cost.split(" ")
            blueprint[robot_type][resource] = int(amount)

    return blueprint

def optimise_blueprint(blueprint):

    #determine most geodes cracked following this blueprint

    #given a branch
    #for each robot we can build
    #simulate time to get enough resources, build it
    #add result back onto branches to explore
    #cut off at 24 minutes

    #branch: (simulated_minutes)

    best_geode_count = 0
    branches = [(0, {"ore": 0}, {"ore": 1})]

    def add_pruned(new_branch):

        [minutes, branch_resources, branch_robots] = new_branch

        #if we made a geode robot every minute until limit, and we still didnt beat best, dont add branch
        remaining = sim_limit - minutes
        if remaining > 0:
            
            robots = 0
            geodes = 0
            if "geode" in branch_robots: robots = branch_robots["geode"]
            if "geode" in branch_resources: geodes = branch_resources["geode"]

            for i in range(0, remaining):
                geodes += robots
                robots += 1

            if geodes <= best_geode_count:
                return
        
        #have we got too many of any robot? if we couldnt spend that many resources, dont add branch
        highestSpend = {}
        for robot_type in robot_types:
            for resource, amount in blueprint[robot_type].items():
                if resource in highestSpend:
                    highestSpend[resource] = max(highestSpend[resource], amount)
                else:
                    highestSpend[resource] = amount

        for robot_type, robot_count in branch_robots.items():
            if robot_type in highestSpend:
                if robot_count > highestSpend[robot_type]:
                    return

        branches.append((minutes, branch_resources, branch_robots))

    n = 0

    while len(branches) > 0:
        [minutes, branch_resources, branch_robots] = branches.pop(0)
        n += 1

        #for each robot type
        for robot_type in robot_types:

            canMakeRobot = True

            #for each resource needed to make this robot
            for resource, amount in blueprint[robot_type].items():
                if not resource in branch_robots: #if we dont produce this resource, skip
                    canMakeRobot = False
                    break

            if canMakeRobot:
                
                #determine how many minutes need simulating until we have enough resources
                simulate = 0
                for resource, amount in blueprint[robot_type].items():
                    needs = amount
                    if resource in branch_resources:
                        needs -= branch_resources[resource]
                    if needs > 0:
                        simulate = max(simulate, math.ceil(needs / branch_robots[resource]))

                #if the robot can be made in time
                if minutes + simulate + 1 <= sim_limit:

                    new_branch_resources = branch_resources.copy()
                    new_branch_robots = branch_robots.copy()

                    #simulate minutes
                    new_minutes = minutes + simulate
                
                    #increment resources
                    for resource, robot_count in branch_robots.items():
                        new_branch_resources[resource] += simulate * robot_count
                    
                    #consume resources
                    for resource, amount in blueprint[robot_type].items():
                        new_branch_resources[resource] -= amount
                    
                    #simulate minute to make robot
                    new_minutes += 1
                    for resource, robot_count in branch_robots.items():
                        new_branch_resources[resource] += 1 * robot_count

                    #make robot
                    if not robot_type in new_branch_resources: new_branch_resources[robot_type] = 0
                    if not robot_type in new_branch_robots: new_branch_robots[robot_type] = 0
                    new_branch_robots[robot_type] += 1

                    #add new branch onto queue
                    add_pruned((new_minutes, new_branch_resources, new_branch_robots))


        #simulate rest of time up to limit
        simulate = sim_limit - minutes

        if simulate > 0:
            minutes += simulate
            for resource, robot_count in branch_robots.items():
                branch_resources[resource] += simulate * robot_count

        #get number of geodes
        if "geode" in branch_resources:
            best_geode_count = max(best_geode_count, branch_resources["geode"])

    return (n, best_geode_count)
                        

quality_sum = 0
for i, line in enumerate(lines, 1):

    blueprint = parse_blueprint(line)
    n, best_geode_count = optimise_blueprint(blueprint)

    print("Blueprint", i, "can make", best_geode_count, " - tested", n, "branches")

    quality = i * best_geode_count
    quality_sum += quality

print("Quality sum:", quality_sum)