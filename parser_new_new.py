import cmath
import math
import numpy as np

file = open("netlist.txt", "r")

def multiplier(value):
    #parses the value into a floating point number assuming it's not AC or an active component
    if value[-1] == 'g':
        #final letter is g so there must be a Meg by the spec, hence we only save everything but the last 3 letters
        return float(value[:-3])*float(10**6)
    elif value[-1]  == 'p':
        return float(value[:-1])*float(10**(-12))
    elif value[-1] == 'n':
        return float(value[:-1])*float(10**(-9))
    elif value[-1] == 'u':
        return float(value[:-1])*float(10**(-6))
    elif value[-1] == 'm':
        return float(value[:-1])*float(10**(-3))
    elif value[-1] == 'k':
        return float(value[:-1])*float(10**3)
    elif value[-1] == 'G':
        return float(value[:-1])*float(10**9)
    else:
        #no multiplier
        return float(value)

class currentSource:
    def __init__(self, label, current, in_node, out_node):
        self.label = label
        self.current = current
        self.in_node = in_node
        self.out_node = out_node

class Resistor:
    def __init__(self, label, conductance, node_1, node_2):
        self.label = label
        self.conductance = conductance
        self.node_1 = node_1
        self.node_2 = node_2

def terminate():
    pass

def parser(file):
    currentSources = []
    conductanceElements = []
    while True:
        line = file.readline()
        if not(line):
            #If we reach the end of the file
            break
        line = line.split() #split line up into a list of individual words
        #We can determine the time of line by looking at the first word
        if line[0] == '*':
        #This is a comment in the netlist, so we just move on to the next line
            pass
        elif line[0] == '.end':
            #This signifies the end of the simulation file
            (nodes, netlistMatrix) = formNetlistMatrix(currentSources, conductanceElements)
            solveMatrix(netlistMatrix, nodes)
        else:
            #This is a component, the way we parse depends on the designator
            designator = line[0][0] #first letter of first word
            if designator == 'I':
                label = line[0]
                in_node = line[1]
                out_node = line[2]
                current = multiplier(line[3])
                currentSources.append(currentSource(label, current, in_node, out_node))
            elif designator == 'R':
                label = line[0]
                node_1 = line[1]
                node_2 = line[2]
                conductance = 1/multiplier(line[3])
                conductanceElements.append(Resistor(label, conductance, node_1, node_2))

def formNetlistMatrix(currentSources, Resistors):
    nodes = []
    for source in currentSources:
        if not(source.in_node in nodes):
            nodes.append(source.in_node)
        if not(source.out_node in nodes):
            nodes.append(source.out_node)
    for resistor in Resistors:
        if not(resistor.node_1 in nodes):
            nodes.append(resistor.node_1)
        if not(resistor.node_2 in nodes):
            nodes.append(resistor.node_2)

    for node in nodes:
        if(node == "0"):
            ground = nodes.index(node)

    new_nodes = [node for node in range(1, len(nodes))]

    row = []
    for source in currentSources:
        if nodes[ground] == source.in_node:
            source.in_node = 0
        if nodes[ground] == source.out_node:
            source.out_node = 0
    for resistor in Resistors:
        if nodes[ground] == resistor.node_1:
            resistor.node_1 = 0
        if nodes[ground] == resistor.node_2:
            resistor.node_2 = 0

    new_nodes.insert(0, 0)

    for node in new_nodes:
        row = []
        for source in currentSources:
            if nodes[node] == source.in_node:
                source.in_node = new_nodes[node]
            if nodes[node] == source.out_node:
                source.out_node = new_nodes[node]
        for resistor in Resistors:
            if nodes[node] == resistor.node_1:
                resistor.node_1 = new_nodes[node]
            if nodes[node] == resistor.node_2:
                resistor.node_2 = new_nodes[node]

    netlistMatrix = []

    for node in new_nodes:
        row = []
        for source in currentSources:
            if (new_nodes[node] == source.in_node):
                row.append(source)
        for resistor in Resistors:
            if (new_nodes[node] == resistor.node_1):
                row.append(resistor)
        netlistMatrix.append(row)
    return (new_nodes, netlistMatrix)

def solveMatrix(netlistMatrix, nodes):
    current = [0 for node in nodes]
    voltages = [None for node in nodes]
    conductance_matrix = [[0 for node in nodes] for node in nodes]
    for node in nodes:
        voltages[node] = "V" + str(node)
        for row in netlistMatrix:
            for component in row:
                if component.label[0] == 'I':
                    if component.out_node == node:
                        current[node] += component.current
                    elif component.in_node == node:
                        current[node] -= component.current
    for node_1 in nodes:
        for node_2 in nodes:
            if node_1 == node_2:
                for row in netlistMatrix:
                    for component in row:
                        if component.label[0] == 'R':
                            conductance_matrix[node_1][node_2] += component.conductance
            else:
                for row in netlistMatrix:
                    for component in row:
                        if component.label[0] == 'R':
                            if ((component.node_1 == node_1) or (component.node_1 == node_2)) and ((component.node_2 == node_1) or (component.node_2 == node_2)):
                                conductance_matrix[node_1][node_2] -= component.conductance
    #To account for ground, we set the first column of the conductance matrix to equal 0 before solving
    current = current[1:]
    if len(current) == 1:
        #we do the below as we can't use solve for 1 dimensional matrices
        conductance_matrix = conductance_matrix[1:]
        x = [0, current[0] * (1/conductance_matrix[0][1])]
    else:
        elimination_matrix = []
        for row in conductance_matrix:
            row = row[1:]
            elimination_matrix.append(row)
        conductance_matrix = np.array(elimination_matrix[1:])
        print(conductance_matrix)
        current = np.array(current)
        x = np.linalg.solve(conductance_matrix,current)
        print(current)
        #https://stackoverflow.com/questions/21761256/insert-element-into-numpy-array
        x = np.insert(x,0,0)
    for node in nodes:
        print(voltages[node] + " = " + str(x[node]))

parser(file)