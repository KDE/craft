from Package.BinaryPackageBase import *
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for version in ['3.3.0']:
            self.targets[ version ] = "http://codesynthesis.com/download/xsd/3.3/windows/i686/xsd-3.3.0-i686-windows.zip"
        self.targetDigests['3.3.0'] = '4d5ed0f88b2ac45fb596b5e56bb1169f3ad19550'

        self.defaultTarget = '3.3.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.withSources = False

    def unpack( self ):
        if not BinaryPackageBase.unpack( self ): return False
        os.renames( os.path.join( self.imageDir(), "xsd-3.3.0-i686-windows", "libxsd" ), os.path.join( self.imageDir(), "include" ) )
        os.renames( os.path.join( self.imageDir(), "xsd-3.3.0-i686-windows", "bin" ), os.path.join( self.imageDir(), "bin" ) )
        shutil.rmtree( os.path.join( self.imageDir(), "xsd-3.3.0-i686-windows" ) )
        return True

if __name__ == '__main__':
    Package().execute()
