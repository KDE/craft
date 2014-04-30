import sys
import os

import utils
import info
import compiler
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['4.7.7'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/external/sip-4.7.7.zip'
        self.targets['4.12.4'] = 'http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.12.4.zip'
        self.targetDigests['4.12.4'] = '01dbf6b37b1daf0ebc31139d4fd7eec48fc2a789'
        self.targetInstSrc['4.12.4'] = 'sip-4.12.4'
        self.defaultTarget = '4.12.4'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        
        self.subinfo.options.configure.defines = ""
        if self.buildType == "Debug":
            self.subinfo.options.configure.defines = " -u"
            
        if compiler.isMSVC2008():
            self.subinfo.options.configure.defines += " -p win32-msvc2008"
        elif compiler.isMSVC2010():
            self.subinfo.options.configure.defines += " -p win32-msvc2010"
        elif compiler.isMinGW():
            self.subinfo.options.configure.defines += " -p win32-g++"
        
        self.subinfo.options.configure.defines += " CFLAGS=-I" +self.packageDir()
        self.subinfo.options.configure.defines += " CXXFLAGS=-I" +self.packageDir()
        
    def configure( self ):
        self.enterSourceDir()
        
        utils.copyFile( os.path.join( self.packageDir(), "win32-msvc2010" ),
                        os.path.join( self.sourceDir(), "specs" ) )

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
        
        # fix problem with not copying manifest file
        if not compiler.isMinGW():
            utils.copyFile( os.path.join( self.sourceDir(), "sipgen", "sip.exe.manifest" ),
                            sys.exec_prefix )

        return True

    def runTest(self):
        return False

