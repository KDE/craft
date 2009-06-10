import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.3.5-2'] = "http://downloads.sourceforge.net/freetype/freetype-2.3.5.tar.bz2"
        self.targets['2.3.7-1'] = "http://downloads.sourceforge.net/freetype/freetype-2.3.7.tar.bz2"
        self.targetInstSrc['2.3.5-2'] = "freetype-2.3.5"
        self.targetInstSrc['2.3.7-1'] = "freetype-2.3.7"
        self.defaultTarget = '2.3.7-1'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        cmd = "cd %s && patch -p1 < %s" % \
              ( os.path.join ( self.workdir, self.instsrcdir ), \
                os.path.join( self.packagedir, "freetype.diff" ) )
        print "cmd: " + cmd
        utils.system( cmd ) or utils.die( "patch" )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( "freetype", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
