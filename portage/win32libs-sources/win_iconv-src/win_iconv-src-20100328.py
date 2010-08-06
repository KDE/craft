import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        self.targets['0.0.1'] = 'http://win-iconv.googlecode.com/files/win-iconv-0.0.1.tar.bz2'
        self.targetInstSrc['0.0.1'] = 'win-iconv-0.0.1'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.options.package.withCompiler = None

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
        if platform.isCrossCompilingEnabled() and self.isTargetBuild():
            self.subinfo.options.configure.defines = "-DBUILD_STATIC=ON "
        
if __name__ == '__main__':
    Package().execute()
