#We want to make a data structure to store each line of the netlist

class line():
    def __init__(self, designator, node0, node1, value, node2=None):
        if designator == "V":

        elif designator == "I":

        elif designator == "R":

        elif designator == "C":

        elif designator == ""



def component_parser(line):
    line = line.split()
    #splits line into each word
    designator = line[0]
    #designator is the first letter of the first word
    node0 = line[1]
    node1 = line[2]
    value = line[-1]
    if len(line)==5:
        node2 = line[3]
    return line(designator, node0 , node1, node2, value)

bob = component_parser(line)
bob.ty