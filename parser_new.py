import random
import cmath
import math

components = []
voltage sources
#each element of the list is a list of form [start node, end node, voltage, current, conductance]

#make an array for every node N001, push all connected to N001, (V-V2)*conductance=(V-V1)*conductance
#Get conductance matrix while doing the above and solve with inverse
#Voltage mat * conductance mat = current
#solve for the voltage array
#voltage mat = inverse of conductance mat * current

#making the easy matrix eqn (dc sources resistor)
#deal with multiple sources
    #finish todayish
#handling complex numbers

#handling non-linear components
    #first step is to write functions to change them into small signal equivalents, lots of iterative loops/numerical methods
#doing ac sweep
    #convert all the dc components to short or open circuit
#DC operating point
    #convert all the ac components to short or open circuit
def matrix_maker(row):
    currents = []
    x = []
    nodes = []

class circuit_matrix:
    def __init__(self):
        nodes = []
        currents = []
    def node_check(self, node):
        if not(node in self.nodes):
            self.nodes.append(node)
    def dc_current(self, in_node, out_node, current):
        self.node_check(in_node)
        self.node_check(out_node)
#frequency

def nodal_analysis(components):
    nodes = []
    node_components = []
    for component in components:
        if not(component[0] in nodes):
            nodes.append(component[0])
    for component in components:
        for node in nodes:
            for other_node in nodes:
                if not(node == other_node):
                    if component[0] == node and component[1]==other_node:
                        #blah
                        voltage = component[2]
                        current =  component[3]
                        conductance = component[4]

                    elif component[0] == other_node and component[1] == node:
                        #blah


def parser(file):
    while True:
        line = file.readline()
        if not(line):
            #If we reach the end of the file
            break
        line = line.split() #split line up into a list of individual words
        #We can determine the time of line by looking at the first word
        if line[0] == '*':
        #This is a comment in the netlist, so we just move on to the next line
        elif line[0] == '.end':
            #This signifies the end of the simulation file
            terminate()
        elif line[0] == '.ac':
            #This formats the numbers  nicely for neat inputs into the AC simulator
            points_per_dec = multiplier(line[2])
            start_freq = multiplier(line[3])
            stop_freq = multiplier(line[4])
            ac_sim(points_per_dec, start_freq, stop_freq)
        else:
            #This is a component, the way we parse depends on the designator
            designator = line[0][0] #first letter of first word
            if designator == 'V':
                plus_node = line[1]
                minus_node = line[2]
                if line[3][0] == 'A':
                    AC = line[3]
                    #AC is of the form "AC(num1 num2)"
                    AC = AC[3:-1].split()
                    #AC is of the form ['num1', 'num2']
                    amplitude = multiplier(AC[0])
                    phase = multiplier(AC[1])
                    ac_voltage(plus_node, minus_node, amplitude, phase)
                else:
                    voltage = multiplier(line[3])
                    dc_voltage(plus_node, minus_node, voltage)
            elif designator == 'I':
                in_node = line[1]
                out_node = line[2]
                if line[3][0] == 'A':
                    AC = line[3]
                    AC = AC[3:-1].split()
                    amplitude = multiplier(AC[0])
                    phase = multiplier(AC[1])
                    ac_current(in_node, out_node, amplitude, phase)
                else:
                    current = multiplier(line[3])
                    dc_current(in_node, out_node, current)
            elif designator == 'R':
                node_1 = line[1]
                node_2 = line[2]
                resistance = multiplier(line[3])
                resistor(node_1, node_2, resistance)
            elif designator == 'C':
                node_1 = line[1]
                node_2 = line[2]
                capacitance = multiplier(line[3])
                capacitor(node_1, node_2, capacitance)
            elif designator == 'L':
                node_1 = line[1]
                node_2 = line[2]
                inductance = multiplier(line[3])
                inductor(node_1, node_2, inductance)
            elif designator == 'D':
                anode = line[1]
                cathode = line[2]
                if line[3] == 'D':
                    si_diode(anode, cathode)
            elif designator == 'Q':
                collector = line[1]
                base = line[2]
                emitter = line[3]
                if line[4] == 'NPN':
                    NPN(collector, base, emitter)
                elif line[4] == 'PNP':
                    PNP(collector, base, emitter)
            elif designator == 'M':
                drain = line[1]
                gate = line[2]
                source = line[3]
                if line[4] == 'NMOS':
                    NMOS(drain, gate, source)
                elif line[4] == 'PMOS':
                    PMOS(drain, gate, source)
            elif designator == 'G':
                plus = line[1]
                minus = line[2]
                control_plus = line[3]
                control_minus = line[4]
                transconductance = multiplier(line[5])
                VCCS(plus, minus, control_minus, control_plus, transconductance)

def terminate():
    return

for each node make a list of components

def ac_sim(points_per_dec, start_freq, stop_freq):
#takes you to another thread
    return

def ac_voltage(plus_node, minus_node, amplitude, phase):
    #polar form, for matrix solving function,
    #for ac, or cartesian form
    #input to solve function, should be able to handle complex numbers
    #make function to handle complex numbers for the solve function
    return

def dc_voltage(plus_node, minus_node, voltage):
    components.push([minus_node, plus_node, voltage, None, None])
    # right side:
    # += voltage
    # left side:
    #  for plus node row
    #   column of plus node = 1, column of minus node = -1, rest of columns = 0
    #  for minus node row
    #   0 for column of plus node

def ac_current(in_node, out_node, amplitude, phase):
    return

def dc_current(in_node, out_node, current):
    #for in_node:
    #right side
    # -= current`
    #for out_node:
    #right side
    # += current

def resistor(in_node, out_node, resistance):
    components.push([in_node, out_node, None, None, 1/resistance])
    #for in_node:
    #   column of out_node -= 1/resistance
    #for out_node:
    #   column of in_node -= 1/resistance

    return

def capacitor(node_1, node_2, capacitance, frequency = frequency):
    conductance = j*frequency*capacitance
    #for in_node:
    #   columns of out_node -= conductance
    #for out_node
    #   columns of in_node -= conductance
    components.push([node_1, node_2, None, None, conductance])

def inductor(node_1, node_2, inductance, frequency = frequency):
    conductance = 1/(j*frequency*inductance)
    # for in_node:
    #   columns of out_node -= conductance
    # for out_node
    #   columns of in_node -= conductance
    components.push([node_1, node_2, None, None, conductance])

def si_diode(anode, cathode):
    i_sat = 0.0075
    v_d = 0.7
    current = i_sat * (math.exp(v_d/0.026)-1)
    components.push([anode, cathode, v_d, current, None])
    #iteratively calculate v_d, assume a value and converge to actual value of v_d
    return current

def NPN(collector, base, emitter):
    beta = 200
    collector_current = si_diode(base, emitter)
    dc_current(collector, emitter, collector_current * beta)

def PNP(collector, base, emitter):
    beta = 200
    base_current = si_diode(emitter, base)
    dc_current(emitter, collector, base_current * beta)

nm_counter = 0

#Remove the FET, find thevenin equivalent, find voltage and current going into MOSFETS and then work out other parameters for the MOSFET


def NMOS(drain, gate, source, nm_counter=nm_counter):
    #assuming enhancement mode
    #http://www.ece.mcgill.ca/~grober4/SPICE/SPICE_Decks/1st_Edition_LTSPICE/chapter5/Chapter%205%20MOSFETs%20web%20version.html
    VCCS(source, drain, source, gate, )
            #enhancement and and saturation mode
            #make function to decide operating mode of the MOSFET


def PMOS(drain, gate, source):
    v_t = -2
    k = 0.0005
    i_d = k * (v_gs - v_t) ^ 2


def VCCS(plus, minus, control_minus, control_plus, transconductance):
    current = (control_plus - control_minus) * transconductance
    dc_current(minus, plus, current)

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
