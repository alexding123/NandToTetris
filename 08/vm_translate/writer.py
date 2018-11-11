class Writer():
    def __init__(self, f):
        self.f = f
        self.call_count = 0

    def set_filename(self, filename):
        self.filename = filename
    
    def write_init(self):
        self.write_comment("Bootstrap code")
        s = "@256\nD=A\n@0\nM=D\n"
        self.f.write(s)
        self.write_call("Sys.init", 0)

    def write_pushpop(self, action, field, address):
        _push_templates = {
            "standard":"@{}\nD=A\n@{}\nA=D+M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static":"@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "constant":"@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp":"@{}\nD=A\n@5\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "pointer":"@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
        }

        _pop_templates = {
            "standard":"@{}\nD=A\n@{}\nD=D+M\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "static":"@SP\nAM=M-1\nD=M\n@{}\nM=D\n",
            "temp":"@{}\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "pointer":"@SP\nAM=M-1\nD=M\n@{}\nM=D\n"
        }
        _field_mapping_M = {"local":"LCL", "argument":"ARG", "this":"THIS", "that":"THAT"}
        if action == "push":
            t = _push_templates
        elif action == "pop":
            t = _pop_templates
        if field == "constant":
            s = t["constant"].format(address)
        elif field in _field_mapping_M:
            s = t["standard"].format(address, _field_mapping_M[field])
        elif field == "static":
            s = t["static"].format("{}.{}".format(self.filename, address))
        elif field == "temp":
            s = t["temp"].format(address)
        elif field == "pointer":
            s = t["pointer"].format("THIS" if address == "0" else "THAT")
        self.f.write(s)

    def write_arithmetic(self, command, count):
        _commands = {
            "add":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D+M\n@SP\nM=M+1\n",
            "sub":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M-D\n@SP\nM=M+1\n",
            "neg":"@SP\nA=M-1\nM=-M\n",
            "and":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D&M\n@SP\nM=M+1\n",
            "or":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D|M\n@SP\nM=M+1\n",
            "not":"@SP\nA=M-1\nM=!M\n"
        }
        _commands_templates = {
            "eq":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=D-M\n@EQ_NOT_{0}\nD;JNE\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n@EQ_END_{0}\n0;JMP\n(EQ_NOT_{0})\n@SP\nA=M\nM=0\n@SP\nM=M+1\n(EQ_END_{0})\n",
            "gt":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@GT_{0}\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@GT_END_{0}\n0;JMP\n(GT_{0})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(GT_END_{0})\n", 
            "lt":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@LT_{0}\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@LT_END_{0}\n0;JMP\n(LT_{0})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(LT_END_{0})\n",
        }
        if command in _commands:
            self.f.write(_commands[command])
        else:
            self.f.write(_commands_templates[command].format(count))

    def write_comment(self, line):
        self.f.write("// " + line + "\n")

    def write_function(self, name, local_count):
        s = "({})\n".format(name)
        self.f.write(s)
        for _ in range(int(local_count)):
            self.write_pushpop("push", "constant", "0")

    def write_call(self, name, parameter_count):
        ret_addr = "{}$RETURN{}".format(name, self.call_count)
        self.call_count += 1
        save_return_addr = "@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(ret_addr)
        save_cond = "@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        arg_reposition = "@SP\nD=M\n@{}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n".format(parameter_count)
        lcl_resposition = "@SP\nD=M\n@LCL\nM=D\n"
        goto = "@{}\n0;JMP\n({})\n".format(name, ret_addr)
        s = save_return_addr + \
        "".join([save_cond.format(space) for space in ["LCL", "ARG", "THIS", "THAT"]]) + \
        arg_reposition + \
        lcl_resposition + \
        goto
        self.f.write(s)
    
    def write_return(self):
        store_endframe = "@LCL\nD=M\n@R14\nM=D\n"
        store_retAddr = "@5\nA=D-A\nD=M\n@R15\nM=D\n"
        self.f.write(store_endframe+store_retAddr)
        self.write_pushpop("pop", "argument", 0)
        restore_SP = "@ARG\nD=M\n@SP\nM=D+1\n"
        restore = "@R14\nAM=M-1\nD=M\n@{}\nM=D\n"
        goto = "@R15\nA=M\n0;JMP\n"
        s = restore_SP + \
        "".join([restore.format(space) for space in ["THAT", "THIS", "ARG", "LCL"]]) + \
        goto
        self.f.write(s)

    def write_label(self, name):
        s = '({})\n'.format(name)
        self.f.write(s)

    def write_goto(self, name):
        s = '@{}\n0;JMP\n'.format(name)
        self.f.write(s)

    def write_if(self, name):
        s = '@SP\nM=M-1\nA=M\nD=M\n@{}\nD;JNE\n'.format(name)
        self.f.write(s)