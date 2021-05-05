#We want to make a data structure to store each line of the netlist

def component_parser(line):
    line = line.split()
    #splits line into each word
    designator = line[0]
    #designator is the first letter of the first word
    node0 = line[1]
    node1 = line[2]