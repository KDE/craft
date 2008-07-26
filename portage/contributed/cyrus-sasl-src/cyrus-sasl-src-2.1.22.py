import base
import utils
import os
import shutil
import info

# see http://wiki.mozilla.org/LDAP_C_SDK_SASL_Windows

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['2.1.22'] = 'ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-2.1.22.tar.gz'
        self.defaultTarget = '2.1.22'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "cyrus-sasl"
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler == "mingw":
            print "error: can only be build with MSVC"
            exit( 1 )

    def unpack( self ):
        base.baseclass.unpack( self ) or utils.die( "unpack failed" )
        os.chdir( self.workdir )
        shutil.move("cyrus-sasl-2.1.22", self.instsrcdir)
        # gnuwin32 patch fails for unknown reason
        patch="c:\\cygwin\\bin\\patch"
        #patch="patch"
        self.system( "cd %s && %s -p0 < %s" % ( os.path.join(self.workdir,self.instsrcdir), patch,os.path.join( self.packagedir, "plugins_NTMakefile.patch" ) ) )
        self.system( "cd %s && %s -p0 < %s" % ( os.path.join(self.workdir,self.instsrcdir), patch,os.path.join( self.packagedir, "utils_NTMakefile.patch" ) ) )
        # required by rc
        fc = open( os.path.join(os.environ["TEMP"],"afxres.h"), "w")
        fc.write("\n")
        fc.close()
        fc = open( os.path.join(self.workdir,self.instsrcdir,"plugins","afxres.h"), "w")
        fc.write("\n")
        fc.close()

        return True

    def compile( self ):
        os.chdir(os.path.join(self.workdir,self.instsrcdir))
        dst = os.path.join( self.imagedir, self.instdestdir)
        # CFG=Release/Debug
        # VERBOSE=0/1
        #DB_INCLUDE
        #DB_LIBPATH
        #OPENSSL_INCLUDE
        #OPENSSL_LIBPATH
        #GSSAPI_INCLUDE
        #GSSAPI_LIBPATH
        #SQLITE_INCLUDE
        #SQLITE_LIBPATH
        #LDAP_LIB_BASE
        #LDAP_INCLUDE
        self.system("nmake /f NTMakefile CFG=%s prefix=%s" % (self.buildType,dst))
        return True

    def install( self ):
        os.chdir(os.path.join(self.workdir,self.instsrcdir))
        dst = os.path.join( self.imagedir, self.instdestdir)
        os.system("nmake /f NTMakefile  CFG=%s prefix=%s install" % (self.buildType,dst))
        return True

    def make_package( self ):

    # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
