from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["2.8.0"] = (
                    "http://ftp.fernuni-hagen.de/ftp-dir/pub/mirrors/www.apache.org//"
                    "xerces/c/2/binaries/xerces"
                    "-c_2_8_0-x86-windows-vc_8_0.zip" )
        self.targetInstSrc["2.8.0"] = "xerces-c_2_8_0-x86-windows-vc_8_0"

        self.targetDigests['2.8.0'] = '15be27c165f1424dcf5c16a01dc9443fe495d676'
        self.shortDescription = "Apache XML Xerces-C parser (http://xerces.apache.org)"
        self.options.package.withCompiler = False
        self.defaultTarget = '2.8.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def compile( self ):
        return True

    def install( self ):
        if( not self.cleanImage()):
            return False

        shutil.copytree(self.sourceDir() , self.installDir())

        return True
if __name__ == '__main__':
    Package().execute()
