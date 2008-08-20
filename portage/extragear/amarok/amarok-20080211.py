import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.80'] = 'tags/amarok/1.80/amarok'
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/amarok'
        self.targets['1.90'] = 'ftp://ftp.kde.org/pub/kde/unstable/amarok/1.90/src/amarok-1.90.tar.bz2'
        self.targetInstSrc['1.90'] = 'amarok-1.90'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/taglib'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['dev-util/ruby'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "amarok"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget == '1.90':
            if( not base.baseclass.unpack( self ) ):
                return False
                
            src = os.path.join( self.workdir, self.instsrcdir )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( src, os.path.join( self.packagedir , "amarok-beta1.diff" ) )
            if utils.verbose() >= 1:
                print cmd
#            self.system( cmd ) or die( "patch" )
            return True
        else:
            return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "amarok", self.buildTarget, True )
        else:
            return self.doPackaging( "amarok", os.path.basename(sys.argv[0]).replace("amarok-", "").replace(".py", ""), True )


if __name__ == '__main__':		
    subclass().execute()
