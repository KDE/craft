import base
import os
import utils
import info

#
# this library is used by kdeedu/kalzium
#

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.1.1'] = 'http://heanet.dl.sourceforge.net/sourceforge/openbabel/openbabel-2.1.1.tar.gz'
        self.targets['2.2.0'] = 'http://heanet.dl.sourceforge.net/sourceforge/openbabel/openbabel-2.2.0.tar.gz'
        self.targetInstSrc['2.1.1'] = 'openbabel-2.1.1'
        self.targetInstSrc['2.2.0'] = 'openbabel-2.2.0'
        self.defaultTarget = '2.2.0'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False

        patch = "openbabel-%s-cmake.diff" % self.buildTarget
        cmd = "cd %s && patch -p0 < %s" % \
              ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir , patch ) )
        if utils.verbose() > 0:
            print cmd
        utils.system( cmd ) or utils.die( "patchin'" )
        
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "openbabel", self.buildTarget )

if __name__ == '__main__':
    subclass().execute()
