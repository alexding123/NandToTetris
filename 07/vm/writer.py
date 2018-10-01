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


def write_pushpop(f, action, field, address, filename):
    if action == "push":
        t = _push_templates
    elif action == "pop":
        t = _pop_templates
    if field == "constant":
        s = t["constant"].format(address)
    elif field in _field_mapping_M:
        s = t["standard"].format(address, _field_mapping_M[field])
    elif field == "static":
        s = t["static"].format("{}.{}".format(filename, address))
    elif field == "temp":
        s = t["temp"].format(address)
    elif field == "pointer":
        s = t["pointer"].format("THIS" if address == "0" else "THAT")
    f.write(s)
_commands = {
    "add":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D+M\n@SP\nM=M+1\n",
    "sub":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M-D\n@SP\nM=M+1\n",
    "neg":"@SP\nA=M-1\nM=-M\n",
    "and":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D&M\n@SP\nM=M+1\n",
    "or":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D|M\n@SP\nM=M+1\n",
    "not":"@SP\nA=M-1\nM=!M\n"
}
_commands_templates = {
    "eq":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=D-M\n@EQ_NOT_{0}\nD;JNE\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n@EQ_END_{0}\n0;JMP\n(EQ_NOT_{0})\n@SP\nA=M\nM=0\n@SP\nM=M+1\n(EQ_END_{0})\n@SP\n",
    "gt":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@GT_{0}\nD;JGT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@GT_END_{0}\n0;JMP\n(GT_{0})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(GT_END_{0})\n@SP\n", #FIX LATER
    "lt":"@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=M-D\n@LT_{0}\nD;JLT\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@LT_END_{0}\n0;JMP\n(LT_{0})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(LT_END_{0})\n@SP\n",
}

def write_arithmetic(f, command, count):
    if command in _commands:
        f.write(_commands[command])
    else:
        f.write(_commands_templates[command].format(count))

def write_comment(f, line):
    f.write("// " + line + "\n")