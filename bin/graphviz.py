# 
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides graphviz tool support"""

import os
import utils
from _winreg import *

class GraphViz:
    def __init__( self, parent=None ):
        self.parent = self
        if parent:
            self.parent = parent
        self.output = False
        if not self.isInstalled():
            utils.system("emerge.bat graphviz");
            if not self.isInstalled():
				utils.die("could not find installed graphviz package, you may download and install it from http://www.graphviz.org/Download.php")

    def isInstalled(self):
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\AT&T Research Labs\Graphviz', 0, KEY_READ)
        except:
            try:
                key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\AT&T Research Labs\Graphviz', 0, KEY_READ)
            except:
                return False
        [self.graphVizInstallPath, type] = QueryValueEx(key, "InstallPath")        
        return True
    
    def system( self, command, errorMessage ):
        if utils.system( command ):
            return True
        else:
            utils.die( "while running %s cmd: %s" % ( errorMessage , str( command ) ) )

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
