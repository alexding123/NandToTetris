import sys 
from pathlib import Path
from writer import Writer
from parser import Parser

if len(sys.argv) != 2:
    print("Usage: python VMTranslator.py file_or_directory_name")
    exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("File/directory {} does not exist.".format(str(p)))
    exit(1)

if p.is_dir():
    files = list(p.glob("*.vm"))
    if len(files) == 0:
        print("No .vm file in directory {}".format(str(p)))
        exit(1)
else:
    files = [p]



with open(p.stem+".asm", "w") as fout:
    w = Writer(fout)
    # check if a Sys.vm file is supplied
    if "Sys" in [f.stem for f in files]:
        w.write_init()
    else:
        print("No Sys.vm found. Skipping sys.init")
    p = Parser()
    for f in files:
        w.set_filename(f.stem)
        with open(f, "r") as fin:
            p.parse(w, fin)