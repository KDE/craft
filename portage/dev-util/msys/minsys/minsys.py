import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '20110309', '20111123' ]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/MSYS-" + ver + ".zip"
            self.patchToApply[ ver ] = ('cd_currentDir.diff', '0')
        self.targetDigests['20110309'] = '3264814e1ef5062f70444ba17b7de147054413b6'
        self.targetDigests['20111123'] = '007d8f3f2fc999f94d98439f05b70109485b3d4f'

        self.shortDescription = 'MinGW-w64 - for 32 and 64 bit Windows'
        self.defaultTarget = '20111123'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
           return False
        utils.copyFile(os.path.join(self.packageDir(),"msys.bat"),os.path.join(self.rootdir,"dev-utils","bin","msys.bat"))
        return True
       
