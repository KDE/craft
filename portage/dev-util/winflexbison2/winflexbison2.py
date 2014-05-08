import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ "2.4.1" ]:
            self.targets[ ver ] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-%s.zip" % ver
        self.targetDigests[ '2.4.1' ] = '1a606bdee53769cfef63825b5175b668e2a815d1'
        self.defaultTarget = "2.4.1"

    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ] = 'default'


from Package.BinaryPackageBase import *


class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.install.installPath = "bin"

    def install( self ):
        if not BinaryPackageBase.install( self ): return False
        return \
            utils.moveFile( os.path.join( self.imageDir( ), "bin", "win_flex.exe" ),
                            os.path.join( self.imageDir( ), "bin", "flex.exe" ) ) and \
            utils.moveFile( os.path.join( self.imageDir( ), "bin", "win_bison.exe" ),
                            os.path.join( self.imageDir( ), "bin", "bison.exe" ) )


