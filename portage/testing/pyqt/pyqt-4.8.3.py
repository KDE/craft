import base
import utils
import sys
import info
import os
import compiler
import sipconfig
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.8.3'] = 'http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-win-gpl-4.8.3.zip'
        self.targetInstSrc['4.8.3'] = 'PyQt-win-gpl-4.8.3'
        self.defaultTarget = '4.8.3'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
        self.subinfo.options.configure.defines = " --confirm-license --verbose"
        if self.buildType == "Debug":
            self.subinfo.options.configure.defines = " -u"
            
        if compiler.isMSVC2008():
            os.putenv( "QMAKESPEC", os.path.join(self.rootdir,"mkspecs","win32-msvc2008") )
        elif compiler.isMSVC2010():
            os.putenv( "QMAKESPEC", os.path.join(self.rootdir,"mkspecs","win32-msvc2010") )
        elif compiler.isMinGW():
            os.putenv( "QMAKESPEC", os.path.join(self.rootdir,"mkspecs","win32-g++") )

    def configure( self ):
        self.enterSourceDir()
        
        cmd = "python configure.py"
        cmd += self.subinfo.options.configure.defines
        os.system(cmd) and utils.die("command: %s failed" % (cmd))

        return True

    def make( self ):
        self.enterSourceDir()
        os.system(self.makeProgramm) and utils.die("command: %s failed" % self.makeProgramm)
        return True

    def install( self ):
        self.enterSourceDir()
        cmd = self.makeProgramm + " install"
        os.system(cmd) and utils.die("command: %s failed" % cmd)
        return True

    def runTest(self):
        return False

if __name__ == '__main__':
    Package().execute()
