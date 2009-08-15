import base
import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.6.0'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.0.zip'
        self.targets['2.6.1'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.1.zip'
        self.targets['2.6.2'] = 'http://www.cmake.org/files/v2.6/cmake-2.6.2.zip'
        self.targetInstSrc['2.6.0'] = 'cmake-2.6.0'
        self.targetInstSrc['2.6.1'] = 'cmake-2.6.1'
        self.targetInstSrc['2.6.2'] = 'cmake-2.6.2'
        self.defaultTarget = '2.6.2'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True

    def execute( self ):
        base.baseclass.execute( self )
        return True
    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        if self.buildTarget == '2.6.1' and not self.compiler == "mingw":
            cmd = "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir , "comsuppw-2.6.1.diff" ) )
            self.system( cmd )
        if self.buildTarget == '2.6.2' and not self.compiler == "mingw":
            cmd = "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir , "comsuppw-2.6.2.diff" ) )
            self.system( cmd )
        return True
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
    # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )
        return True
if __name__ == '__main__':
    subclass().execute()
