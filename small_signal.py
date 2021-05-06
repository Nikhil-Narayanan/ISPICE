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

class bjt:
    def __init__(self, collector, base, emitter, model):
        self.collector = collector
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


#Make a data structure with the information of all the small signal parameters