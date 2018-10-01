from .writer import write_arithmetic, write_pushpop, write_comment

def clean_line(l):
    l = l[:-1]
    if l.find("//") != -1:
        return ""
    return l
def parse(fin, fout, name):
    i = 0
    for l in fin.readlines():
        l = clean_line(l)
        if l == "": continue
        write_comment(fout, l)
        keys = l.split(" ")
        if len(keys) == 3:
            write_pushpop(fout, keys[0], keys[1], keys[2], name)
        elif len(keys) == 1:
            write_arithmetic(fout, keys[0], i)
        i += 1
