import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        self.targets['0.0.1'] = 'http://win-iconv.googlecode.com/files/win-iconv-0.0.1.tar.bz2'
        self.targetDigests['0.0.1'] = 'faf4f1f311f92f2a80afe275f43fabb047f23308'
        self.targetInstSrc['0.0.1'] = 'win-iconv-0.0.1'
        if platform.isCrossCompilingEnabled():
            self.defaultTarget = 'svnHEAD'
        else:
            self.defaultTarget = '0.0.1'

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
