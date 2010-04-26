import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.44'] =  self.getUnifiedPackage( 'http://downloads.sourceforge.net/kde-windows' , "pexports" , '0.44' ,packagetypes=['bin'] )
        self.targetDigests['0.44'] = 'dd9497260e89c25e51f120de41949a09f08ee54f'
        self.defaultTarget = '0.44'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True


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



