import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'libical'
        for v in [ '0.41', '0.42', '0.43', '0.44']:
            self.targets[ v ] = 'http://downloads.sourceforge.net/freeassociation/libical-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libical-' + v
        self.defaultTarget = '0.44'
        self.targetDigests['0.44'] = 'f781150e2d98806e91b7e0bee02abdc6baf9ac7d'
        self.patchToApply['0.44'] = ( 'libical-0.44-20100728.diff', 1 )
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false "
        
        if platform.isCrossCompilingEnabled() and self.isTargetBuild():
            self.subinfo.options.configure.defines += " -DSTATIC_LIBRARY=ON "

if __name__ == '__main__':
    Package().execute()
