import base
import os
import shutil
import utils
from utils import die
import info

#
# this library is used by kdeedu/kstars
# the library is c-only 
#
class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.12.1'] = 'http://downloads.sourceforge.net/libnova/libnova-0.12.1.tar.gz'
        self.targets['0.12.3'] = 'http://downloads.sourceforge.net/libnova/libnova-0.12.3.tar.gz'
        self.targetInstSrc['0.12.1'] = 'libnova-0.12.1'
        self.targetInstSrc['0.12.3'] = 'libnova-0.12.3'
        self.defaultTarget = '0.12.3'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW right now."
            exit( 1 )

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False

        cmd = "cd %s && patch -p1 < %s" % \
              ( os.path.join( self.workdir, self.instsrcdir ),
                os.path.join( self.packagedir , "libnova.diff" ) )
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) or die
        return True

    def compile( self ):
        return self.msysCompile()

    def install( self ):
        return self.msysInstall()

    def make_package( self ):
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        libname = "libnova-" + self.buildTarget.replace('.', '-')
        self.stripLibs( libname )
        self.createImportLibs( libname )
        # now do packaging with kdewin-packager
        self.doPackaging( "libnova", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
