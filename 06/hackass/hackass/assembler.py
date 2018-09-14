from pathlib import Path
from .parser import first_pass, second_pass
from .symboltable import table, new_var
def assemble(path):
    file_name = path.stem
    with open(path, "r") as f:
        first_pass(f, table)
    with open(path, "r") as f:
        with open(file_name+".hack", "w") as g:
            second_pass(f, g, table)
            

