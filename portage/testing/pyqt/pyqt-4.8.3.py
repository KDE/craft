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
        self.targetDigests['4.8.3'] = '737e6ff98a4c0e5149035733928203b12d09a247'
        self.defaultTarget = '4.8.3'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        # jom reports missing moc_translator.xxx
        self.subinfo.options.make.supportsMultijob = False
        # add support for other location based on pythonpath
        self.subinfo.options.merge.destinationPath = "emerge/python"
        
        self.subinfo.options.configure.defines = " --confirm-license --verbose"
        if self.buildType == "Debug":
            self.subinfo.options.configure.defines = " -u"
            
        if compiler.isMSVC2008():
            os.putenv( "QMAKESPEC", os.path.join(self.mergeDestinationDir(),"mkspecs","win32-msvc2008") )
        elif compiler.isMSVC2010():
            os.putenv( "QMAKESPEC", os.path.join(self.mergeDestinationDir(),"mkspecs","win32-msvc2010") )
        elif compiler.isMinGW():
            os.putenv( "QMAKESPEC", os.path.join(self.mergeDestinationDir(),"mkspecs","win32-g++") )

    def configure( self ):
        self.enterSourceDir()
        
        cmd = "python configure.py"
        cmd += self.subinfo.options.configure.defines
        cmd += " --bindir %s/bin " % self.installDir() 
        cmd += " --destdir %s/Lib/site-packages/PyQt4 " % self.installDir() 
        cmd += " --plugin-destdir %s/plugins " % self.installDir() 
        cmd += " --sipdir %s/sip/PyQt4 " % self.installDir() 
        
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
