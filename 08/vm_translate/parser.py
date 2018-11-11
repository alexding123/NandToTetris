def clean_line(l):
    l = l[:-1] # remove \n
    i = l.find("//")
    if i != -1:
        l = l[:i]
    return l.rstrip()

class Parser():
    def __init__(self):
        self.line_count = 0
    def parse(self, w, fin):
        for l in fin.readlines():
            l = clean_line(l)
            if l == "": continue
            w.write_comment(l) # for debug only
            keys = l.split(" ")
            if len(keys) == 3:
                if keys[0] == "function":
                    w.write_function(keys[1], keys[2])
                elif keys[0] == "call":
                    w.write_call(keys[1], keys[2])
                else:
                    w.write_pushpop(keys[0], keys[1], keys[2])
            elif len(keys) == 2:
                if keys[0] == "label":
                    w.write_label(keys[1])
                elif keys[0] == "goto":
                    w.write_goto(keys[1])
                elif keys[0] == "if-goto":
                    w.write_if(keys[1])
            elif len(keys) == 1:
                if keys[0] == "return":
                    w.write_return()
                else:
                    w.write_arithmetic(keys[0], self.line_count)
            self.line_count += 1