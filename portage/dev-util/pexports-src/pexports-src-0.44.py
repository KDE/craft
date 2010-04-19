import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.44'] = 'http://tml.pp.fi/pexports-0.44.zip'
        self.targetDigests['0.44'] = 'd40111ba34330dbbcea459d3b915f3406f840807'
        self.defaultTarget = '0.44'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/bison'] = 'default'
        self.hardDependencies['gnuwin32/flex'] = 'default'
        
        
from Package.MakeFilePackageBase import *        
        
class Package(MakeFilePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.unpack.unpackToBuildDir = True
        self.subinfo.options.make.ignoreErrors = True
        self.subinfo.options.make.makeOptions = "LEX=flex"
        MakeFilePackageBase.__init__( self )

    def unpack( self ):
        if not MakeFilePackageBase.unpack( self ):
            return False
        return True

    def install( self ):
        # there is no install target in the Makefile
        destDir = os.path.join( self.installDir(), "bin" )
        utils.createDir( destDir )
        utils.copyFile(os.path.join( self.buildDir(),  "pexports.exe" ), os.path.join( destDir ,"pexports.exe" ) )
        return True

if __name__ == '__main__':
    Package().execute()


