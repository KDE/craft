import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'libical'
        for v in [ '0.41', '0.42', '0.43', '0.44']:
            self.targets[ v ] = 'http://downloads.sourceforge.net/freeassociation/libical-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libical-' + v
        self.defaultTarget = '0.44'
        self.patchToApply['0.44'] = ( 'libical-src-0.44.patch', 0 )
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.package.withCompiler = None
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false "

if __name__ == '__main__':
    Package().execute()
