STATIC = "static"
FIELD = "field"
ARG = "arg"
VAR = "var"

class SymbolTable:
    """ Symbol table that stores a class-level table and 
        a subroutine-level table as dictionaries
        Each entry is indexed by variable name and is a 
        tuple of the form (type, kind, #)
    """

    def __init__(self):
        self.classST = {}
        self.subST = {}
        # current count of each kind of variable
        self._index = {STATIC:0, FIELD:0, ARG:0, VAR:0} 
    
    def start_subroutine(self):
        self.subST = {}
        self._index[ARG] = 0
        self._index[VAR] = 0
    
    def define(self, name, type, kind):
        if kind in (STATIC, FIELD):
            self.classST[name] = (type, kind, self._index[kind])
        else:
            self.subST[name] = (type, kind, self._index[kind])

        self._index[kind] += 1
    
    def var_count(self, kind):
        return self._index[kind]
    
    def kind_of(self, name):
        if name in self.subST:
            return self.subST[name][1]
        elif name in self.classST:
            return self.classST[name][1]
        else:
            return None

    def type_of(self, name):
        if name in self.subST:
            return self.subST[name][0]
        elif name in self.classST:
            return self.classST[name][0]
        else:
            raise Exception("Variable {} has not been defined".format(name))
    
    def index_of(self, name):
        if name in self.subST:
            return self.subST[name][2]
        elif name in self.classST:
            return self.classST[name][2]
        else:
            raise Exception("Variable {} has not been defined".format(name))
            