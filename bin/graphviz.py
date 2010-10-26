# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides graphviz tool support"""

import os
import utils
from _winreg import *

class GraphViz:
    def __init__(self,parent):
        self.parent = parent
        self.output = False
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\AT&T Research Labs\Graphviz', 0, KEY_READ)
        except:
            try:
                key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\AT&T Research Labs\Graphviz', 0, KEY_READ)
                print key
            except:
                # @todo triggers installing of dev-utils/graphviz package 
                utils.die("could not find installed graphviz package, you may download and install it from http://www.graphviz.org/Download.php")
        [self.graphVizInstallPath, type] = QueryValueEx(key, "InstallPath")        
    
    def runDot(self, inFile, outFile, dotFormat="pdf"):
        dotExecutable= os.path.join(self.graphVizInstallPath,'bin','dot.exe')
        self.outFile = outFile
        if not self.parent.system("\"%s\" -T%s -o%s %s" % (dotExecutable, dotFormat, outFile, inFile), "create %s" % outFile):
            self.output = False
            return false
        else:
            self.output = True
            return True
    
    def openOutput(self):
        if self.output:
            return self.parent.system("start %s " % self.outFile, "start %s" % self.outFile)
        else:
            return False
