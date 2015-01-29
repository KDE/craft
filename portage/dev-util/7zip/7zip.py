import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['938']:
            self.targets[ ver ] = "http://www.7-zip.org/a/7z%s-extra.7z" % ver
            self.targetInstallPath[ ver ] = "bin"
    
        self.targetDigests['938'] = '089d6bddd45614dd543a32b12f54b17eeee5764c'
        self.defaultTarget = '938'


    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True


    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.rmtree(os.path.join( self.imageDir(), "bin", "Far"))
        if compiler.isX64():
            for f in os.listdir( self.imageDir() ):
                name = os.path.join( self.imageDir(), f)
                if os.path.isfile(name):
                    utils.deleteFile(name)
            utils.moveEntries(os.path.join( self.imageDir(), "bin", "x64"), os.path.join(self.imageDir(), "bin"))
        utils.rmtree(os.path.join( self.imageDir(), "bin", "x64"))
        return True

        

