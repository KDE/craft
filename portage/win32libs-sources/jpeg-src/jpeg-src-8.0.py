import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['7.0'] = "http://www.ijg.org/files/jpegsrc.v7.tar.gz"
        self.targetInstSrc['7.0'] = "jpeg-7"
        self.targets['8.0'] = "http://www.ijg.org/files/jpegsrc.v8.tar.gz"
        self.targetInstSrc['8.0'] = "jpeg-8"
        self.patchToApply['7.0'] = ( 'jpeg7.diff', 1 )
        self.patchToApply['8.0'] = ( 'jpeg8.diff', 1 )

        self.defaultTarget = '7.0'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()