import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.targets['0.1.0'] = 'http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-0.1.0.tar.gz'
        self.targetInstSrc['0.1.0'] = 'qtscriptgenerator-src-0.1.0'
        #patches = [ "qtscriptgenerator-cmake.diff",1]
        #patches.append(["qtscriptgenerator.diff",1])
        # \todo there is only one patch possible
        #self.patchToApply['0.1.0'] = patches
        self.defaultTarget = '0.1.0'
   
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "qtscriptgenerator-cmake.diff" ), 1)
        utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "qtscriptgenerator.diff" ), 1)
        return True

if __name__ == '__main__':
    Package().execute()
