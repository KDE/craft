#
# copyright (c) 2010 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides graphviz tool support"""

import os
import utils
try:
    from _winreg import *
    HAS_REGISTRY = True
except ImportError:
    import subprocess
    HAS_REGISTRY = False


def getUnixInstalledDot():
    """Figures out the path to dot on a unixoid system"""
    try:
        p = subprocess.Popen(["which", "dot"], stdout=subprocess.PIPE)
        path = p.communicate()
        return None if p.returncode != 0 else path[0].strip()
    except OSError:
        return None


def getWindowsInstalledDot():
    """Uses the Windows registry to find the path to dot.exe"""
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\AT&T Research Labs\Graphviz', 0, KEY_READ)
    except WindowsError:
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Wow6432Node\AT&T Research Labs\Graphviz', 0, KEY_READ)
        except WindowsError:
            return False
    return os.path.join(QueryValueEx(key, "InstallPath")[0], 'bin', 'dot.exe')


class GraphViz:
    def __init__( self, parent=None ):
        self.parent = self
        if parent:
            self.parent = parent
        self.output = False
        self.outFile = None
        self.graphVizInstallPath = None
        if not self.isInstalled():
            utils.system("emerge.bat graphviz")
            if not self.isInstalled():
                utils.die("could not find installed graphviz package, you may download and install it from http://www.graphviz.org/Download.php")

    def isInstalled(self):
        if HAS_REGISTRY:
            self.graphVizInstallPath = getWindowsInstalledDot()
        else:
            self.graphVizInstallPath = getUnixInstalledDot()
        return self.graphVizInstallPath is not None


    def system( self, command, errorMessage ):
        if utils.system( command ):
            return True
        else:
            utils.die( "while running %s cmd: %s" % ( errorMessage, str( command ) ) )

    def runDot(self, inFile, outFile, dotFormat="pdf"):
        dotExecutable = self.graphVizInstallPath
        self.outFile = outFile
        if not self.parent.system("\"%s\" -T%s -o%s %s" % (dotExecutable, dotFormat, outFile, inFile), "create %s" % outFile):
            self.output = False
            return False
        else:
            self.output = True
            return True

    def openOutput(self):
        if self.output:
            return self.parent.system("start %s " % self.outFile, "start %s" % self.outFile)
        else:
            return False
