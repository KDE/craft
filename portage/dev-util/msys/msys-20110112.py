import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20110112"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/MSYS-"+ver+".zip"
        self.defaultTarget = ver
        self.targetDigests['20110112'] = '6217b5d38acb6a8c1efb25847be62d61c1f18083'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(),"msys.bat"),os.path.join(self.rootdir,"dev-utils","bin","msys.bat"))
        return True
if __name__ == '__main__':
    Package().execute()
