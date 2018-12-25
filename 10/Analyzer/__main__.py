from tokenizer import Tokenizer
from compilationengine import CompilationEngine
import sys

USAGE = """Jack syntax analyzer. 

Usage: 
  Analyzer <name>
  Analyzer <directory_name>

"""

if len(sys.argv) != 2:
    print(USAGE)
    sys.exit(1)

from pathlib import Path

p = Path(sys.argv[1])
if p.is_dir():
    files = p.glob("*.jack")
    for f in files:
        CompilationEngine(f, p / "{}.xml".format(f.stem))
else:
    if p.suffix != ".jack":
        print("{} is not a .jack file".format(p.name))
    else:
        CompilationEngine(p, "{}.xml".format(p.stem))