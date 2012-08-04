import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.62'] = "http://the.earth.li/~sgtatham/putty/latest/x86/putty.zip"
        self.targetDigests['0.62'] = '953e7b2eb7844184ccfb24651c7829f3e1e30558'
        self.targetInstallPath['0.62'] = "bin"
        self.defaultTarget = '0.62'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()



