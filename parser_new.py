import random

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

def terminate():
    return

def ac_sim(points_per_dec, start_freq, stop_freq):
    return

def ac_voltage(plus_node, minus_node, amplitude, phase):
    return

def dc_voltage(plus_node, minus_node, voltage):
    return

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
