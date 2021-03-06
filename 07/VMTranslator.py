import sys 
from pathlib import Path
from vm.parser import parse

if len(sys.argv) != 2:
    print("Usage: python VMTranslator.py fileName.vm")
    exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("File {} does not exist.".format(str(p)))
    exit(1)

file_name = p.stem
with open(p, "r") as fin:
    with open(file_name+".asm", "w") as fout:
        parse(fin, fout, file_name)