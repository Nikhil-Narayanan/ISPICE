#Creates small signal equivalent of circuit

#Make a class for each component
class Vs:
    def __init__(self, plus, minus, value):
        self.plus = plus
        self.minus = minus
        self.value = value

class Is:
    def __init__(self, inp, out, value):
        self.inp = inp
        self.out = out
        self.value = value

class diode:
    def __init__(self, anode, cathode, model):
        self.anode = anode
        self.cathode = cathode
        self.model = model

class mosfet:
    def __init__(self, source, gate, drain, model):
        self.source = source
        self.gate = gate
        self.drain = drain
        self.model = model

class bjt:
    def __init__(self, collector, base, emitter, model):
        self.collector = source
        self.base = base
        self.emitter = emitter
        self.model = model

class res:
    def __init__(self, value):
        self.value = value

class ind:
    def __init__(self, value):
        self.value = value

class cap:
    def __init__(self, value):
        self.value = value

class vccs:
    def __init__(self, plus, minus, ctrlp, ctrlm, transc):
        self.collector = source
        self.base = base
        self.emitter = emitter
        self.model = model
#Make a data structure with the information of all the small signal parameters

class Graph:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for i in range(V)]

    # add edge to graph
    def addEdge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    # Returns count of edge in undirected graph
    def countEdges(self):
        Sum = 0

        # traverse all vertex
        for i in range(self.V):
            # add all edge that are linked
            # to the current vertex
            Sum += len(self.adj[i])

            # The count of edge is always even
        # because in undirected graph every edge
        # is connected twice between two vertices
        return Sum // 2
