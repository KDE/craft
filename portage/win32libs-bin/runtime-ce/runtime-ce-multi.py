import info
import os
import os.path
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['9.0release'] = ""
        self.targets['9.0debug'] = ""
        if EmergeBase().buildType() == "Debug":
            self.defaultTarget = '9.0debug'
        else:
            self.defaultTarget = '9.0release'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        if not compiler.isMSVC():
            utils.die("Only Microsoft Visual Studio is currently "+
                       "supported for getting the ce runtime.")

    def unpack(self):
        ''' Copy the runtime files from the Visual Studio directory into
            the image dir of the package '''
        if not os.path.isdir( os.environ["VSDIR"] ):
            utils.die("Could not find Visual Studio. "
                      " Please make sure that %%VSDIR%% is set correctly.")
        runtime = os.path.join( os.environ["VSDIR"], "VC", "ce", "dll",
                                "armv4i" )

        if EmergeBase().buildType() == "Debug":
            runtime = os.path.join(runtime, "msvcr90d.dll")
        else:
            runtime = os.path.join(runtime, "msvcr90.dll")

        if not os.path.isfile(runtime):
            utils.die("No CRT found at: %s " % runtime)

        destdir = os.path.join(self.installDir(), "bin")
        if not os.path.isdir(destdir):
            os.makedirs(destdir)
        utils.debug("copyining crt files into image root %s" % destdir,1)
        utils.copyFile( runtime, destdir )
        return True

if __name__ == '__main__':
    Package().execute()
