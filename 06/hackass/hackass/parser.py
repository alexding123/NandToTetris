from .code import a_translate, c_translate
from .symboltable import new_var

def clean_line(s):
    s = s.replace(" ", "")
    s = s.replace("\n", "")
    comment_index = s.find("//")
    if comment_index != -1:
        s = s[:comment_index]
    return s # returns empty string if empty line

def first_pass(f, symbol_table):
    line_no = 0 # counter for current code line number
    for l in f.readlines():
        l = clean_line(l)
        if l == "": # ignore empty lines
            continue
        if l[0] == "(":
            i = l.find(")")
            symbol_table[l[1:i]] = line_no
        else:
            line_no += 1

def writeline(f, l):
    f.write(l+"\n")

def second_pass(fin, fout, symbol_table):
    for l in fin.readlines():
        l = clean_line(l)
        if l == "" or l[0] == True or l[0] == "(":
            continue
        if l[0] == "@": # a command
            value = l[1:]
            if not value.isnumeric(): # is special symbol
                if value in symbol_table: # if already in, just get value
                    writeline(fout, a_translate(symbol_table[value]))
                else:
                    value = new_var(value) # add new entry into table
                    writeline(fout, a_translate(value))
            else:
                writeline(fout, a_translate(int(value)))
        else: # c command
            # parse it into three parts
            eql_index = l.find("=")
            dest = "null"
            if eql_index != -1: # 
                dest = l[:eql_index]
            semi_index = l.find(";")
            comp = ""
            jump = "null"
            if semi_index == -1:
                comp = l[eql_index+1:]
            else:
                comp = l[eql_index+1:semi_index]
                jump = l[semi_index+1:]
            writeline(fout, c_translate(dest, comp, jump))

