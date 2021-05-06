#We want to make a data structure to store each line of the netlist

class component():
    def __init__(self, designator, node0, node1, value, node2=None):
        self.designator = designator
        self.node0 = node0
        self.node1 = node1
        self.value = value
        if not(node2 == None):
            self.node2 = node2

def ac_analysis():
    return

def terminate():
    return

def component_parser(line):
    designator = line[0]
    #designator is the first letter of the first word
    node0 = line[1]
    node1 = line[2]
    value = line[-1]
    if len(line)==5:
        node2 = line[3]
    return component(designator, node0 , node1, node2, value)

def simulation_parser(line):
    if line[0] == '.ac':
        return ac_analysis()
    if line[0] == '.end':
        return terminate()

def interpreter(line):
    line = line.split()
    if line[0][0]=='.':
        return simulation_parser(line)
    else:
        return component_parser(line)

file1 = open('netlist.txt', 'w')
count = 0

while True:
    count += 1

    # Get next line from file
    line = file1.readline()

    # if line is empty
    # end of file is reached
    if not line:
        break
    interpreter(line)