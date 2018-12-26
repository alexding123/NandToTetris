class VMWriter:
    def __init__(self, fout):
        self.f = open(fout, "w")
    
    def write_push(self, segment, index):
        self.f.write("{} {} {}\n".format("push", segment, index))
    
    def write_pop(self, segment, index):
        self.f.write("{} {} {}\n".format("pop", segment, index))
    
    def write_arithmetic(self, op):
        self.write_command(op)
    
    def write_label(self, label):
        self.write_command("label", label)
    
    def write_goto(self, label):
        self.write_command("goto", label)
    
    def write_if(self, label):
        self.write_command("if-goto", label)
    
    def write_call(self, name, n_args):
        self.write_command("call", name, n_args)

    def write_function(self, name, n_locals):
        self.write_command("function", name, n_locals)
    
    def write_return(self):
        self.write_command("return")

    def write_command(self, command, arg1="", arg2=""):
        self.f.write("{} {} {}\n".format(command, arg1, arg2))

    def close(self):
        self.f.close()