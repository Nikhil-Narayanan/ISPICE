import random
import cmath
import math

components = []
#each element of the list is a list of form [start node, end node, voltage, current, conductance]

frequency

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

def ac_sim(points_per_dec, start_freq, stop_freq):
#takes you to another thread
    return

def ac_voltage(plus_node, minus_node, amplitude, phase):
    return

def dc_voltage(plus_node, minus_node, voltage):
    components.push([minus_node, plus_node, voltage, None, None])
    return

def ac_current(in_node, out_node, amplitude, phase):
    return

def dc_current(in_node, out_node, current):
    components.push([in_node, out_node, None, current, None])
    return

def resistor(in_node, out_node, resistance):
    components.push([in_node, out_node, None, None, 1/resistance])
    return

def capacitor(node_1, node_2, capacitance, frequency = frequency):
    conductance = j*frequency*capacitance
    components.push([node_1, node_2, None, None, conductance])

def inductor(node_1, node_2, inductance, frequency = frequency):
    conductance = 1/(j*frequency*inductance)
    components.push([node_1, node_2, None, None, conductance])

def si_diode(anode, cathode):
    i_sat = 0.0075
    v_d = 0.7
    current = i_sat * (math.exp(v_d/0.026)-1)
    components.push([anode, cathode, v_d, current, None])
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

def NMOS(drain, gate, source, nm_counter=nm_counter):
    #assuming enhancement mode
    #http://www.ece.mcgill.ca/~grober4/SPICE/SPICE_Decks/1st_Edition_LTSPICE/chapter5/Chapter%205%20MOSFETs%20web%20version.html
    VCCS(source, drain, source, gate, )


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
