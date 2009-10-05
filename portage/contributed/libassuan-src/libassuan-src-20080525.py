import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['1.0.5'] = 'ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-1.0.5.tar.bz2'
        self.defaultTarget = '1.0.5'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "libassuan"
        self.subinfo = subinfo()

    def unpack( self ):
        if self.buildTarget == "svnHEAD":
            if utils.verbose() >= 1:
                print "libassuan unpack called"
            # do the svn fetch/update
            repo = "svn://cvs.gnupg.org/libassuan/trunk"
            self.svnFetch( repo )

            utils.cleanDirectory( self.workdir )

            # now copy the tree below destdir/trunk to workdir
            srcdir = os.path.join( self.svndir, "trunk" )
            destdir = os.path.join( self.workdir, "libassuan" )
            utils.copySrcDirToDestDir( srcdir, destdir )

            os.chdir( self.workdir )
            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan.diff" ) ) )
            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan-cmake.diff" ) ) )

            return True
        else:
            base.baseclass.unpack( self ) or utils.die( "unpack failed" )
            os.chdir( self.workdir )
            shutil.move("libassuan-1.0.5", "libassuan")
            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan.diff" ) ) )
            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan-cmake.diff" ) ) )
            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan-unistd.diff" ) ) )
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
