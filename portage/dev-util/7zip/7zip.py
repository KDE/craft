import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        if compiler.isX64():
            self.targets['938'] = "http://winkde.org/~pvonreth/downloads/winkde/7za-938-x64.zip"
            self.targetDigests['938'] = '479036267973def3943aff826b847a15d70882f5'
        else:
            self.targets['938'] = "http://winkde.org/~pvonreth/downloads/winkde/7za-938-x86.zip"
        self.targetInstallPath['938'] = "bin"
        self.defaultTarget = '938'


    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True



        

