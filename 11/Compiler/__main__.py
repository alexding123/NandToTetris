from compilation_engine import CompilationEngine
import sys

USAGE = """Jack compiler. 

Usage: 
  Compiler <file_name>
  Compiler <directory_name>

"""

if len(sys.argv) != 2:
    print(USAGE)
    sys.exit(1)

from pathlib import Path

p = Path(sys.argv[1])
if p.is_dir():
    files = p.glob("*.jack")
    for f in files:
        CompilationEngine(f, p / "{}.vm".format(f.stem))
else:
    if p.suffix != ".jack":
        print("{} is not a .jack file".format(p.name))
    else:
        CompilationEngine(p, "{}.vm".format(p.stem))