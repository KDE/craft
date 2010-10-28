import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        for ver in ['0.0.1', '0.0.2']:
            self.targets[ver] = 'http://win-iconv.googlecode.com/files/win-iconv-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'win-iconv-' + ver

        self.targetDigests['0.0.1'] = 'faf4f1f311f92f2a80afe275f43fabb047f23308'
        self.targetDigests['0.0.2'] = 'd61714a4708d76537600782eb72ccb3cbc89b4b5'

        self.defaultTarget = '0.0.2'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
        if platform.isCrossCompilingEnabled() and self.isTargetBuild():
            self.subinfo.options.configure.defines = "-DBUILD_STATIC=ON "
        
if __name__ == '__main__':
    Package().execute()
