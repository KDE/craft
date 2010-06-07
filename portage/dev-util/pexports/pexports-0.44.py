import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.44'] =  self.getUnifiedPackage( 'http://downloads.sourceforge.net/kde-windows' , "pexports" , '0.44' ,packagetypes=['bin'] )
        self.defaultTarget = '0.44'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget']       = 'default'

from Package.BinaryPackageBase import *        
        
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()



