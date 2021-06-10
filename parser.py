import numpy as np

file = open("netlist.txt", "r")

class voltageSource:
    def __init__(self, label, voltage, plus_node, minus_node):
        self.label = label
        self.voltage = voltage
        self.plus_node = plus_node
        self.minus_node = minus_node


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

def multiplier(value):
    # parses the value into a floating point number assuming it's not AC or an active component
    if value[-1] == 'g':
        # final letter is g so there must be a Meg by the spec, hence we only save everything but the last 3 letters
        return float(value[:-3]) * float(10 ** 6)
    elif value[-1] == 'p':
        return float(value[:-1]) * float(10 ** (-12))
    elif value[-1] == 'n':
        return float(value[:-1]) * float(10 ** (-9))
    elif value[-1] == 'u':
        return float(value[:-1]) * float(10 ** (-6))
    elif value[-1] == 'm':
        return float(value[:-1]) * float(10 ** (-3))
    elif value[-1] == 'k':
        return float(value[:-1]) * float(10 ** 3)
    elif value[-1] == 'G':
        return float(value[:-1]) * float(10 ** 9)
    else:
        # no multiplier
        return float(value)

def terminate():
    pass


def parser(file):
    voltageSources = []
    currentSources = []
    conductanceElements = []
    while True:
        line = file.readline()
        if not (line):
            # If we reach the end of the file
            break
        line = line.split()  # split line up into a list of individual words
        # We can determine the time of line by looking at the first word
        if line[0] == '*':
            # This is a comment in the netlist, so we just move on to the next line
            pass
        elif line[0] == '.end':
            # This signifies the end of the simulation file
            (nodes, netlistMatrix) = formNetlistMatrix(currentSources, voltageSources, conductanceElements)
            solveMatrix(netlistMatrix, nodes, voltageSources)
        else:
            # This is a component, the way we parse depends on the designator
            designator = line[0][0]  # first letter of first word
            if designator == 'I':
                label = line[0]
                in_node = line[1]
                out_node = line[2]
                current = multiplier(line[3])
                currentSources.append(currentSource(label, current, in_node, out_node))
            elif designator == 'V':
                label = line[0]
                plus_node = line[1]
                minus_node = line[2]
                voltage = multiplier(line[3])
                voltageSources.append(voltageSource(label, voltage, plus_node, minus_node))
            elif designator == 'R':
                label = line[0]
                node_1 = line[1]
                node_2 = line[2]
                conductance = 1 / multiplier(line[3])
                conductanceElements.append(Resistor(label, conductance, node_1, node_2))


def formNetlistMatrix(currentSources, voltageSources, Resistors):
    nodes = []
    for source in currentSources:
        if not (source.in_node in nodes):
            nodes.append(source.in_node)
        if not (source.out_node in nodes):
            nodes.append(source.out_node)
    for resistor in Resistors:
        if not (resistor.node_1 in nodes):
            nodes.append(resistor.node_1)
        if not (resistor.node_2 in nodes):
            nodes.append(resistor.node_2)
    for voltageSource in voltageSources:
        if not (voltageSource.plus_node in nodes):
            nodes.append(voltageSource.plus_node)
        if not (voltageSource.minus_node in nodes):
            nodes.append(voltageSource.minus_node)

    nodes.sort()

    new_nodes = [node for node in range(0, len(nodes))]

    for node in new_nodes:
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
        for voltageSource in voltageSources:
            if nodes[node] == voltageSource.plus_node:
                voltageSource.plus_node = new_nodes[node]
            if nodes[node] == voltageSource.minus_node:
                voltageSource.minus_node = new_nodes[node]

    netlistMatrix = []

    for node in new_nodes:
        row = []
        for source in currentSources:
            if ((new_nodes[node] == source.in_node) or (new_nodes[node] == source.out_node)):
                row.append(source)
        for resistor in Resistors:
            if ((new_nodes[node] == resistor.node_1) or (new_nodes[node] == resistor.node_2)):
                row.append(resistor)
        for voltageSource in voltageSources:
            if (new_nodes[node == voltageSource.plus_node]):
                row.append(voltageSource)
        netlistMatrix.append(row)
    return (new_nodes, netlistMatrix)


def constructMatrixG(nodes, netlistMatrix):
    nodes = nodes[1:]
    conductance_matrix = [[0 for node in nodes] for node in nodes]
    for node_1 in nodes:
        for node_2 in nodes:
            if (node_1 == node_2):
                for row in netlistMatrix:
                    for component in row:
                        if (component.label[0] == 'R'):
                            if ((((component.node_1 == node_1) or (component.node_1 == node_2)) and (
                                    (component.node_2 == node_1) or (component.node_2 == node_2))) or (
                                    (node_1 == node_2) and (
                                    (component.node_1 == node_1) or (component.node_2 == node_1)))):
                                conductance_matrix[node_1 - 1][node_2 - 1] += component.conductance
            else:
                for row in netlistMatrix:
                    for component in row:
                        if component.label[0] == 'R':
                            if ((component.node_1 == node_1) or (component.node_1 == node_2)) and (
                                    (component.node_2 == node_1) or (component.node_2 == node_2)):
                                conductance_matrix[node_1 - 1][node_2 - 1] += -component.conductance
    return np.array(conductance_matrix) * 0.5

def constructMatrixB(nodes, voltageSources):
    nodes = nodes[1:]
    B = [[0 for voltageSource in voltageSources] for node in nodes]
    for i in range(len(voltageSources)):
        for j in range(len(nodes)):
            if (voltageSources[i].minus_node == nodes[j]):
                B[j][i] = -1
            if (voltageSources[i].plus_node == nodes[j]):
                B[j][i] = 1
    return np.array(B)

def constructMatrixC(nodes, voltageSources):
   B = constructMatrixB(nodes, voltageSources)
   C = B.transpose()
   return C * 0.5

def constructMatrixD(voltageSources):
    D = [[0 for voltageSource in voltageSources] for voltageSource in voltageSources]
    return np.array(D)

def constructMatrixA(nodes, netlistMatrix, voltageSources):
    G = constructMatrixG(nodes, netlistMatrix)
    B = constructMatrixB(nodes, voltageSources)
    C = constructMatrixC(nodes, voltageSources)
    D = constructMatrixD(voltageSources)
    U = np.concatenate((G,B), axis = 1)
    L = []
    if(not(len(voltageSources) == 0)):
        L = np.concatenate((C,D), axis = 1)
        A = np.concatenate((U,L), axis = 0)
        return A
    return U



def constructMatrixV(nodes):
    nodes = nodes[1:]
    return ["V" + str(node) for node in nodes]

def constructMatrixJ(voltageSources):
    return ["I_" + voltageSource.label for voltageSource in voltageSources]

def constructMatrixX(nodes, voltageSources):
    V = constructMatrixV(nodes)
    J = constructMatrixJ(voltageSources)
    X = V + J
    return X


def constructMatrixI(nodes, netlistMatrix):
    currents = [0 for node in nodes]
    for node in nodes:
        for row in netlistMatrix:
            for component in row:
                if component.label[0] == 'I':
                    if component.out_node == node:
                        currents[node] += component.current
                    elif component.in_node == node:
                        currents[node] -= component.current
    currents = currents[1:]
    return np.array(currents)

def constructMatrixE(voltageSources):
    E = []
    for voltageSource in voltageSources:
        E.append(voltageSource.voltage)
    return np.array(E)

def constructMatrixZ(nodes, netlistMatrix, voltageSources):
    E = constructMatrixE(voltageSources)
    I = constructMatrixI(nodes, netlistMatrix)
    Z = np.concatenate((I,E), axis = 0)
    return np.array(Z)

def sortVoltage(voltageSources):
    voltageStrings = []
    for voltageSource in voltageSources:
        voltageStrings.append(voltageSource.label)
    voltageStrings.sort()
    newVoltageSources = []
    for i in range(len(voltageSources)):
        if voltageSources[i].label == voltageStrings[i]:
            newVoltageSources.append(voltageSources[i])
    return newVoltageSources

def solveMatrix(netlistMatrix, nodes, voltageSources):
    voltageSources = sortVoltage(voltageSources)
    A = constructMatrixA(nodes, netlistMatrix, voltageSources)
    X = constructMatrixX(nodes, voltageSources)
    Z = constructMatrixZ(nodes, netlistMatrix, voltageSources)
    Solution = np.linalg.solve(A, Z) * 0.5
    for node in range(len(nodes) - 1 + len(voltageSources)):
        print(X[node] + " = " + str(Solution[node]))


parser(file)