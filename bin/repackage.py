import sys
import os

def usage():
    print()
    print("can be used to repackage a packagelist")
    print("Syntax:")
    print("\t", sys.argv[0], "packagelist.txt")


if len(sys.argv) == 1:
    usage()
    exit(1)

if not os.path.exists(sys.argv[1]):
    print("error: couldn't find packagelist file", sys.argv[1])
    usage()
    exit(1)

cmdtemplate = "emerge --package%s %s/%s"
targettemplate = " --target=%s"
patchleveltemplate = " --patchlevel=%s"
with open(sys.argv[1], 'rb') as f:
    for line in f:
        if line.startswith('#'):
            continue
        cat,pac,target,patchlevel = line.strip().split(',')
        patchlevel_target = ""
        if target:
            patchlevel_target = targettemplate % target
        if patchlevel:
            patchlevel_target += patchleveltemplate % patchlevel
        cmd = cmdtemplate % (patchlevel_target, cat, pac)
        print("running cmd:", cmd)
        os.system(cmd)
        
