from pathlib import Path
from hackass import assemble
import sys

if len(sys.argv) != 2:
    print("Usage: python hackass.py <file_path>")
    exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("Path {} does not exist".format(p))
    exit(1)

assemble(p)
print("Translation successful")