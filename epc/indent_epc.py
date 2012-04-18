import json
import sys

if len(sys.argv)<2:
    sys.exit(1)
sys.argv.pop(0)
inFile = sys.argv.pop(0)
epc = open(inFile,"rt+")
tmp = json.load(epc)
epc.close()
epc = open(inFile,"wt+",newline='\n')
epc.write(json.dumps(tmp,indent = 2,sort_keys=True))
epc.close()