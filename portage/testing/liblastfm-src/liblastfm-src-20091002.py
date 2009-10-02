import os
import info
import shutil

from Package.QMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://github.com/mxcl/liblastfm.git"
        self.options.package.packageName = "liblastfm"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['testing/libfftw'] = 'default'
        self.hardDependencies['testing/libsamplerate'] = 'default'

# How to build liblastfm even without the newest commercial ATL SDK:
# (everything that follows has been tried in 279712d5215633ab0c3f3c5b38d2597d78416fb8 of the github git repo)
# 1) install ruby and make sure it is in the path
# 2) install the windows platform SDK 2003 R2 and set the environment variable PSDKDIR to the platform sdk directory
# 3) go into C:\Program Files\Microsoft Platform....R2\Include\atl\atlbase.h and 
#    comment out the lines containing #pragma comment(lib, "atl.lib") and 
#    #pragma comment(lib, "atlthunk.lib")
# 4) run emerge -i liblastfm-src

# please keep in mind that this package behaves differently and that --update is not supported
# also you should run 


class Package(QMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        if "PSDKDIR" in os.environ:
            os.environ["PSDKDIR"] = os.environ["PSDKDIR"].replace('\\', '/')
        else:
            print "it won't work!!!!!!!!!!!!!!!!!"
        QMakePackageBase.__init__( self )

    def unpack( self ):
        QMakePackageBase.unpack( self )
        self.source.shell.execute( self.sourceDir(), "git", "reset --hard" )
        ret = utils.applyPatch( self.sourceDir(), os.path.join( self.packageDir(), "liblastfm-fixes.diff" ) , "1" )
        return ret
        
    def configure( self ):
        old_dir = os.getcwd()
        os.chdir( self.sourceDir() )
        cmd = "ruby " + os.path.join( self.sourceDir(), "configure" ) + " --skip-checks --prefix \\"
        ret = self.system( cmd )
        os.chdir( old_dir )
        return ret

    def make( self ):
        old_dir = os.getcwd()
        os.chdir( self.sourceDir() )
        ret = self.system( self.makeProgramm + " all" )
        os.chdir( old_dir )
        return ret

    def install( self ):
        old_dir = os.getcwd()
        os.chdir( self.sourceDir() )
        ret = self.system( self.makeProgramm + " install DESTDIR=" + self.imageDir() + '\\' )
        ret = ret and self.system( self.makeProgramm + " clean" )
        os.chdir( self.imageDir() )
        if not os.path.exists( os.path.join( self.imageDir(), "bin" ) ):
            os.mkdir( os.path.join( self.imageDir(), "bin" ) )
        shutil.move( os.path.join( "lib", "lastfm.dll" ), os.path.join( "bin", "lastfm.dll" ) )
        shutil.move( os.path.join( "lib", "lastfm_fingerprint.dll" ), os.path.join( "bin", "lastfm_fingerprint.dll" ) )
        os.chdir( old_dir )
        return ret

if __name__ == '__main__':
    Package().execute()
