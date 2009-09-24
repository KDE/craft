import base
import os
import shutil
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.0-beta1'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta1.tar.bz2'
        self.targets['4.0-beta2'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta2.tar.bz2'
        self.targets['4.0-beta4'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta4.tar.bz2'
        self.targets['4.0-beta7'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta7.tar.bz2'
        self.targets['4.0-beta8'] = 'http://downloads.sourceforge.net/libmsn/libmsn-4.0-beta8.tar.bz2'
        self.targetInstSrc['4.0-beta1'] = 'libmsn-4.0-beta1'
        self.targetInstSrc['4.0-beta2'] = 'libmsn-4.0-beta2'
        self.targetInstSrc['4.0-beta4'] = 'libmsn-4.0-beta4'
        self.targetInstSrc['4.0-beta7'] = 'libmsn-4.0-beta7'
        self.targetInstSrc['4.0-beta8'] = 'libmsn-4.0-beta8'
        self.defaultTarget = '4.0-beta8'
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/openssl'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        if self.buildTarget == '4.0-beta1':
            cmd = "cd %s && patch -p0 < %s" % \
                  ( self.workdir, os.path.join( self.packagedir , "libmsn.diff" ) )
            if utils.verbose() >= 1:
                print cmd
            self.system( cmd ) or die( "patch" )
        if self.buildTarget == '4.0-beta2':
            cmd = "cd %s && patch -p0 < %s" % \
                  ( self.workdir, os.path.join( self.packagedir , "libmsn_b2.diff" ) )
            if utils.verbose() >= 1:
                print cmd
            self.system( cmd ) or die( "patch" )
        if self.buildTarget == '4.0-beta4':
            cmd = "cd %s && patch -p0 < %s" % \
                  ( self.workdir, os.path.join( self.packagedir , "libmsn_b4.diff" ) )
            if utils.verbose() >= 1:
                print cmd
            self.system( cmd ) or die( "patch" )

        return True
        

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        if not self.kdeInstall():
            return False
        return True

    def make_package( self ):
        # now do packaging with kdewin-packager
        self.doPackaging( "libmsn", self.buildTarget, True )
        return True
  
if __name__ == '__main__':
    subclass().execute()
