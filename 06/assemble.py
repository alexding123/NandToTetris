import sys
import hackass
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python assemble.py file_name")
    exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("File {} does not exist.".format(str(p)))
    exit(1)

hackass.assemble(p)