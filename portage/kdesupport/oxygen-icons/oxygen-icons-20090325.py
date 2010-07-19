import info

class subinfo(info.infoclass):

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/oxygen-icons'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/oxygen-icons'
        self.defaultTarget = 'svnHEAD'
        
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        # this package could be used for all build types (only images) 
        ## \todo find a way to reuse this build output for different build types
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.useBuildType = False
        self.subinfo.options.useCompilerType = False
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
