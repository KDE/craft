import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.8g'] = 'ftp://sunsite.cnlab-switch.ch/mirror/openssl/source/openssl-0.9.8g.tar.gz'
        self.targetInstSrc['0.9.8g'] = 'openssl-0.9.8g'
        self.svnTargets['svnHEAD'] = False
        self.defaultTarget = '0.9.8g'
    
    def setDependencies( self ):
        self.hardDependency['dev-util/perl'] = 'default'

# if you update openssl please make sure that the install section contains an error - please make double sure that you get all stuff
    

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def compile( self ):
        if self.compiler == "mingw":
            compiler = "mingw32"
        else:
            compiler = "do_ms"
        workdir = os.path.join( self.workdir, self.instsrcdir )
        cmd = 'cd %s && ms\\%s' % ( workdir, compiler )
        print cmd
        utils.system( cmd ) or utils.die( "failed on command: %s" % cmd )
        return True

    def install( self ):
        workdir = os.path.join( self.workdir, self.instsrcdir )
        utils.cleanDirectory( os.path.join( self.imagedir, "bin" ) )
        utils.cleanDirectory( os.path.join( self.imagedir, "lib" ) )
        utils.cleanDirectory( os.path.join( self.imagedir, "include" ) )
        # instead of being written to out32dll the dll's go to the root - this might change
        shutil.copy( os.path.join( workdir, "libeay32.dll" ), os.path.join( self.imagedir, "bin" ) )
        shutil.copy( os.path.join( workdir, "libssl32.dll" ), os.path.join( self.imagedir, "bin" ) )
        if self.compiler == "mingw":
            shutil.copy( os.path.join( workdir, "out", "libeay32.a" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libssl32.a" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libcrypto.a" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libssl.a" ), os.path.join( self.imagedir, "lib" ) )
        else:
            # this is not tested yet - I have no msvc build currently 
            shutil.copy( os.path.join( workdir, "out", "libeay32.lib" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libssl32.lib" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libcrypto.lib" ), os.path.join( self.imagedir, "lib" ) )
            shutil.copy( os.path.join( workdir, "out", "libssl.lib" ), os.path.join( self.imagedir, "lib" ) )
        
        shutil.copytree( os.path.join( workdir, "outinc", "openssl" ), os.path.join( self.imagedir, "include", "openssl" ) )
        return True

    def make_package( self ):
        # clean directory
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        for lib in PACKAGE_DLL_NAME.split():
            self.stripLibs( lib )

        # auto-create both import libs with the help of pexports
        for lib in PACKAGE_DLL_NAME.split():
            self.createImportLibs( lib )

        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
