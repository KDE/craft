import sys
import os
import argparse


usage = "%(prog)s -f list.txt\n" \
        "   or: %(prog)s --file=list.txt \n"
parser = argparse.ArgumentParser(prog=sys.argv[0], usage=usage)

parser.add_argument("-f", "--file", dest = "filename", metavar = "list.txt",
                    help="the filename for a packagelist")
parser.add_argument("-t", "--type", action = "store", default = OUTPUT_DOT,
        help="Change the output format type possible values: xml kwi, dot")

args, rest = parser.parse_known_args()

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

if not hasattr(args, "filename") or args.filename != None or not os.path.exists(args.filename):
    print("error: couldn't find packagelist or can't read it")
    parser.print_help()
    exit(1)

filename = args.filename

cmdtemplate = "emerge --package%s %s/%s"
targettemplate = " --target=%s"
patchleveltemplate = " --patchlevel=%s"



with open(sys.argv[1], 'r') as f:
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
        
