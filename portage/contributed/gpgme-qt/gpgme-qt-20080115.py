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

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        # cmake scripts are not in src root...
        self.instsrcdir = "gpgme-qt"

    def unpack( self ):
        print "gpgme-qt unpack called"
        # do the svn fetch/update
        repo = "svn://cvs.gnupg.org/gpgme/trunk/gpgme"
        self.svnFetch( repo )

        utils.cleanDirectory( self.workdir )

        # now copy the tree below destdir/trunk to workdir
        print self.svndir, self.workdir
        srcdir = os.path.join( self.svndir )
        destdir = os.path.join( self.workdir, "gpgme-qt" )
        utils.copySrcDirToDestDir( srcdir, destdir )

        os.chdir( self.workdir )
        self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "gpgme-qt.patch" ) ) )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):

        # now do packaging with kdewin-packager
        self.doPackaging( "gpgme-qt", "svn", True )

        return True
    
if __name__ == '__main__':
    subclass().execute()
