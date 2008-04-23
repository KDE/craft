import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir="lyx/development/cmake"
        self.subinfo = subinfo()

    def unpack( self ):
        if utils.verbose() >= 1:
            print "lyx unpack called"
        # do the svn fetch/update
        repo = "svn://svn.lyx.org/lyx/lyx-devel/trunk"
        self.svnFetch( repo )

        utils.cleanDirectory( self.workdir )

        # now copy the tree below destdir/trunk to workdir
        srcdir = os.path.join( self.svndir, "trunk" )
        destdir = os.path.join( self.workdir, "lyx" )
        utils.copySrcDirToDestDir( srcdir, destdir )

        os.chdir( self.workdir )
#            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan.diff" ) ) )
#            self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "libassuan-cmake.diff" ) ) )
#    os.system( "patch -p0 < libassuan_cmake.diff" )

        return True

    def compile( self ):
        self.kdeCustomDefines = " -DGNUWIN32_DIR=" + self.rootdir
        self.kdeCustomDefines += " -Daspell=1"
        if os.getenv("KDECOMPILER") == "mingw":
            self.kdeCustomDefines += " -Dmerge=0"
            self.kdeCustomDefines += " -DCONFIGURECHECKS=1"
        else:
            self.kdeCustomDefines += " -Dmerge=1"
            self.kdeCustomDefines += " -DCONFIGURECHECKS=0"
        self.kdeCustomDefines += " -Dnls=1"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):

    # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
