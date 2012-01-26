import os
import sys
import subprocess

import portage

__doc__ = """this script produces a fetchlist for wget to synchronize the
win32libs packages from sourceforge by asking emerge with --geturls.
You must run this script for each compiler and add the fetchlist outputfile
file as a second parameter. New urls will get appended to the fetchlist, so
you must make sure that you start with an empty fetchlist file."""

if not len(sys.argv) == 3:
    print("wrong number of arguments")
    print()
    print("syntax:")
    print(sys.argv[0] + " packageListFile.txt outputfile")
    print()
    print(__doc__)
    exit(1)

_packageListFile = open(sys.argv[1])
_fetchListFile = open(sys.argv[2], "a+b")

os.environ["EMERGE_SOURCEONLY"] = "False"
os.environ["EMERGE_PACKAGETYPES"] = "dbg,src"
for line in _packageListFile:
    if line.startswith('#'): continue
    
    _cat, _pac, _ver, _patch = line.split(",")
    cat, pac = portage.PortageInstance.getCorrespondingBinaryPackage(_pac)
    if cat == None or pac == None:
        continue

    cmd = "emerge -q --geturls " + cat + "/" + pac
    try:
        output = subprocess.check_output(cmd.split(' '), shell=True)
    except:
        continue
    print(output)
    _fetchListFile.write(output)