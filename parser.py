import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file = open("netlist.txt", "r")

class voltageSource:
    def __init__(self, label, voltage, plus_node, minus_node, ac_bool, op_bool):
        self.label = label
        self.voltage = voltage
        self.plus_node = plus_node
        self.minus_node = minus_node
        self.ac_bool = ac_bool
        self.op_bool = op_bool
    def update_voltage(self):
        #think about whether this is necessary, pls
        if self.ac_bool:
            if self.op_bool:
                self.voltage = 0
                return self.voltage
            else:
                return self.voltage
        else:
            if self.op_bool:
                return self.voltage
            else:
                self.voltage = 0
                return self.voltage

class currentSource:
    def __init__(self, label, current, in_node, out_node, ac_bool, op_bool):
        self.label = label
        self.current = current
        self.in_node = in_node
        self.out_node = out_node
        self.ac_bool = ac_bool
        self.op_bool = op_bool
    def update_current(self):
        if self.ac_bool:
            if self.op_bool:
                self.current = 0
                return self.current
            else:
                return self.current
        else:
            if self.op_bool:
                return self.current
            else:
                self.current = 0
                return self.current


class Resistor:
    def __init__(self, label, conductance, node_1, node_2):
        self.label = label
        self.conductance = conductance
        self.node_1 = node_1
        self.node_2 = node_2

class Inductor:
    def __init__(self, label, conductance, node_1, node_2):
        self.label = label
        self.conductance = conductance
        self.node_1 = node_1
        self.node_2 = node_2
    def update_conductance(self, omega):
        self.conductance = self.conductance / omega
        return self.conductance
    def reset_conductance(self, omega):
        self.conductance = self.conductance / omega
        return self.conductance

class Capacitor:
    def __init__(self, label, conductance, node_1, node_2):
        self.label = label
        self.conductance = conductance
        self.node_1 = node_1
        self.node_2 = node_2
    def update_conductance(self, omega):
        self.conductance = self.conductance * omega
        return self.conductance
    def reset_conductance(self, omega):
        self.conductance = self.conductance / omega
        return self.conductance

#solve DC op point with ac = 0
#solve ac by removing dc values

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

def multiplier_tester_func():
    #here is a function I made to test the multiplier, it works as expected
    while True:
        prefix = ['p', 'n', 'u', 'm', 'k', 'Meg', 'G', '']
        num = random.randrange(-1000,1000)
        num = str(num) + prefix[random.randint(0,7)]
        print(num)
        print(multiplier(num))
        check = input("Enter N if wrong: ")
        if(check == "N"):
            break

def terminate():
    pass

def frequency_generator(start_freq, stop_freq, points_per_decade):
    frequencies = []
    frequency = 0
    n = 0
    while(frequency <= stop_freq):
        frequency = 10**(n/points_per_decade)*start_freq
        n = n + 1
        frequencies.append(frequency)
    return frequencies

#for dc make it a really small frequency

#take frequencies
#find DC .op
#find ac values
#output/input, VR1/V1 for every freq in the sweep, only magnitude
#ask in terminal for output and input nodes/sources
#first source input, last line output

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
            terminate()
        elif line[0] == '.op':
            frequency = 0.000000000000000000000000000000000001
            print('DC OPERATING POINT')
            (nodes, netlistMatrix) = formNetlistMatrix(currentSources, voltageSources, conductanceElements, frequency, True)
            solveMatrix(netlistMatrix, nodes, voltageSources)
        elif line[0] == '.ac':
            points_per_dec = multiplier(line[2])
            start_freq = multiplier(line[3])
            stop_freq = multiplier(line[4])
            frequencies = frequency_generator(start_freq, stop_freq, points_per_dec)
            magnitudes = []
            for frequency in frequencies:
                (nodes, netlistMatrix) = formNetlistMatrix(currentSources, voltageSources, conductanceElements, frequency, False)
                magnitudes.append(solveMatrix(netlistMatrix, nodes, voltageSources))
                for conductanceElement in conductanceElements:
                    if ((conductanceElement.label[0] == 'C') or (conductanceElement.label[0] == 'L')):
                        conductanceElement.reset_conductance(2*np.pi*frequency)
            magnitudes = 20 * np.log10(magnitudes)
            d = {'Frequency (Hz)': frequencies, 'Gain (dB)': magnitudes}
            df = pd.DataFrame(data = d)
            print(df)
            (nodes, netlistMatrix) = formNetlistMatrix(currentSources, voltageSources, conductanceElements, 12, False)
            sns.set_style("darkgrid")
            sns.set_context("paper")
            sns.lineplot(x='Frequency (Hz)', y='Gain (dB)', data=df)
            plt.xscale('log')
            plt.ylim(None, 3)
            plt.title("Frequency Response", fontsize=14, weight='bold')
            plt.show()

            #put magnitudes and frequencies on the matlab script
        else:
            # This is a component, the way we parse depends on the designator
            designator = line[0][0]  # first letter of first word
            if designator == 'I':
                label = line[0]
                in_node = line[1]
                out_node = line[2]
                ac_bool = line[3][0] == 'A'
                if ac_bool:
                    amplitude = multiplier(line[4][1:])
                    phase = np.deg2rad(multiplier(line[5][:-1]))
                    current = np.complex(amplitude * np.cos(phase), amplitude * np.sin(phase))
                else:
                    current = multiplier(line[3])
                currentSources.append(currentSource(label, current, in_node, out_node, ac_bool, False))
            elif designator == 'V':
                label = line[0]
                plus_node = line[1]
                minus_node = line[2]
                ac_bool = line[3][0] == 'A'
                if ac_bool:
                    amplitude = multiplier(line[4][1:])
                    phase = np.deg2rad(multiplier(line[5][:-1]))
                    voltage = np.complex(amplitude * np.cos(phase), amplitude * np.sin(phase))
                else:
                    voltage = multiplier(line[3])
                voltageSources.append(voltageSource(label, voltage, plus_node, minus_node, ac_bool, False))
            elif designator == 'R':
                label = line[0]
                node_1 = line[1]
                node_2 = line[2]
                conductance = 1 / multiplier(line[3])
                conductanceElements.append(Resistor(label, conductance, node_1, node_2))
            elif designator == 'L':
                label = line[0]
                node_1 = line[1]
                node_2 = line[2]
                #assume initially that omega is 1, f=0 for dc analysis
                conductance = 1 /(1j * multiplier(line[3]))
                conductanceElements.append(Inductor(label, conductance, node_1, node_2))
            elif designator == 'C':
                label = line[0]
                node_1 = line[1]
                node_2 = line[2]
                #assume initially that omega is 1, 2pif
                conductance = 1j * multiplier(line[3])
                print(conductance)
                conductanceElements.append(Capacitor(label, conductance, node_1, node_2))
            elif designator == 'D':
                anode = line[1]
                cathode = line[2]
                if line[3] == 'D':
                    #blah
                    pass
            elif designator == 'Q':
                collector = line[1]
                base = line[2]
                emitter = line[3]
                if line[4] == 'NPN':
                    #NPN
                    pass
                elif line[4] == 'PNP':
                    #PNP
                    pass
            elif designator == 'M':
                drain = line[1]
                gate = line[2]
                source = line[3]
                if line[4] == 'NMOS':
                    #NMOS
                    pass
                elif line[4] == 'PMOS':
                    #PMOS
                    pass
            elif designator == 'G':
                plus = line[1]
                minus = line[2]
                control_plus = line[3]
                control_minus = line[4]
                transconductance = multiplier(line[5])
                #Make changes to matrix G
                #VCCS
                #current = (control_plus - control_minus) * transconductance
                #dc_current(minus, plus, current)

def formNetlistMatrix(currentSources, voltageSources, conductanceElements, frequency, op_bool):
    nodes = []
    for source in currentSources:
        if not (source.in_node in nodes):
            nodes.append(source.in_node)
        if not (source.out_node in nodes):
            nodes.append(source.out_node)
        if op_bool:
            source.op_bool = True
        source.update_current()
    for conductanceElement in conductanceElements:
        if not (conductanceElement.node_1 in nodes):
            nodes.append(conductanceElement.node_1)
        if not (conductanceElement.node_2 in nodes):
            nodes.append(conductanceElement.node_2)
        #below we adjust the conductance element by frequency
        if((conductanceElement.label[0] == 'C') or (conductanceElement.label[0] == 'L')):
            conductanceElement.update_conductance(frequency*2*np.pi)
    for voltageSource in voltageSources:
        if not (voltageSource.plus_node in nodes):
            nodes.append(voltageSource.plus_node)
        if not (voltageSource.minus_node in nodes):
            nodes.append(voltageSource.minus_node)
        if op_bool:
            voltageSource.op_bool = True
        voltageSource.update_voltage()

    nodes.sort()

    new_nodes = [node for node in range(0, len(nodes))]

    for node in new_nodes:
        for source in currentSources:
            if nodes[node] == source.in_node:
                source.in_node = new_nodes[node]
            if nodes[node] == source.out_node:
                source.out_node = new_nodes[node]
        for conductanceElement in conductanceElements:
            if nodes[node] == conductanceElement.node_1:
                conductanceElement.node_1 = new_nodes[node]
            if nodes[node] == conductanceElement.node_2:
                conductanceElement.node_2 = new_nodes[node]
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
        for conductanceElement in conductanceElements:
            if ((new_nodes[node] == conductanceElement.node_1) or (new_nodes[node] == conductanceElement.node_2)):
                row.append(conductanceElement)
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
                        if (component.label[0] == 'R') or (component.label[0] == 'C') or (component.label[0] == 'L'):
                            if ((((component.node_1 == node_1) or (component.node_1 == node_2)) and (
                                    (component.node_2 == node_1) or (component.node_2 == node_2))) or (
                                    (node_1 == node_2) and (
                                    (component.node_1 == node_1) or (component.node_2 == node_1)))):
                                conductance_matrix[node_1 - 1][node_2 - 1] += component.conductance
            else:
                for row in netlistMatrix:
                    for component in row:
                        if (component.label[0] == 'R') or (component.label[0] == 'C') or (component.label[0] == 'L'):
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
   return C

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
    node_1 = voltageSources[0].plus_node
    node_2 = voltageSources[0].minus_node
    bool_notground = False
    for element in range(len(nodes)):
        if (X[element] == "V" + str(node_1)):
            voltage_1 = Solution[element]
            bool_notground = True
    if bool_notground == False:
        voltage_1 = 0
    bool_notground = False
    for element in range(len(nodes)):
        if (X[element] == "V" + str(node_2)):
            voltage_2 = Solution[element]
            bool_notground = True
    if bool_notground == False:
        voltage_2 = 0
    input_voltage = voltage_2 - voltage_1
    index1 = 0
    index2 = 0
    component = netlistMatrix[index1][index2]
    row = netlistMatrix[index1]
    while(component.label[0] == 'V') or (component.label[0] == 'I'):
        if row == []:
            index1 = index1 + 1
            row = netlistMatrix[index1]
        else:
            row.pop(index2)
            index2 = index2 + 1
            component = row[index2]
    output_node = component.node_1
    print(output_node)
    for node in range(len(nodes) - 1):
        if(node + 1 == output_node):
            output_voltage = Solution[node]
    for element in range(len(nodes) - 1 + len(voltageSources)):
        print(X[element] + " = " + str(Solution[element]))
    return np.absolute(output_voltage/input_voltage)

parser(file)