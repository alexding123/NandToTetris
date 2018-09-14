table = {"SP":0, "LCL":1, "ARG":2, "THIS":3, "THAT":4,
           "SCREEN": 16384, "KBD": 24576}

for i in range(16):
    table["R"+str(i)] = i

_current_var = 16

def new_var(s):
    global table, _current_var
    table[s] = _current_var
    _current_var += 1
    return _current_var-1