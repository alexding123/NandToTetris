import sys 
from pathlib import Path
from vm_translate import translate
if len(sys.argv) != 2:
    print("Usage: python VMTranslator.py file_or_directory_name")
    exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("File {} does not exist.".format(str(p)))
    exit(1)
file_name = p.stem
with open(file_name+".asm", "w") as fout:
    vm_translate.translate(p, fout)