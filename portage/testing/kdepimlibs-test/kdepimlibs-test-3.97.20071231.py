import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepimlibs'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdepimlibs"
        self.nocopy = False
        os.environ["EMERGE_NOCOPY"] = "False"
        self.subinfo = subinfo()

    def unpack( self ):
#        print "gpgme-qt unpack called"
        # do the svn fetch/update
        repo = "svn://cvs.gnupg.org/gpgme/trunk/gpgme"

        utils.cleanDirectory( self.workdir )

        self.svnFetch( repo )
        self.kdeSvnUnpack()
        
        srcdir = os.path.join( self.svndir )
        destdir = os.path.join( self.workdir, "kdepimlibs", "gpgme-qt" )
        utils.copySrcDirToDestDir( srcdir, destdir )

        os.chdir( self.workdir )
        utils.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "gpgme-qt.patch" ) ) )
        return True

    def compile( self ):
        # add env var so that boost headers are found
        path = os.path.join( self.rootdir, "win32libs" )
        os.putenv( "BOOST_ROOT", path )

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdepimlibs", os.path.basename(sys.argv[0]).replace("kdepimlibs-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
