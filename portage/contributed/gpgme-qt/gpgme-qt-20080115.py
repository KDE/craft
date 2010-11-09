import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['r1322'] = "http://saroengels.net/kde-windows/gnuwin32/gpgme-qt.tar.bz2"
        self.targetInstSrc['r1322'] = "gpgme-qt"
        self.defaultTarget = 'r1322'
     
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['dev-util/automoc'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
        if not os.getenv("KDECOMPILER") == "mingw":
            self.hardDependencies['kdesupport/kdewin'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        # cmake scripts are not in src root...
        self.instsrcdir = "gpgme-qt"
        self.subinfo = subinfo()

    def unpack( self ):
        print "gpgme-qt unpack called"
        # do the svn fetch/update
        if self.buildTarget == 'svnHEAD':
            repo = "svn://cvs.gnupg.org/gpgme/trunk/gpgme"
            self.svnFetch( repo )

            utils.cleanDirectory( self.workdir )

            # now copy the tree below destdir/trunk to workdir
            utils.debug( "%s %s" % ( self.svndir, self.workdir ) )
            srcdir = os.path.join( self.svndir )
            destdir = os.path.join( self.workdir, "gpgme-qt" )
            utils.copySrcDirToDestDir( srcdir, destdir )
        else:
            if( not base.baseclass.unpack( self ) ):
                return True

        os.chdir( self.workdir )
        self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "gpgme-qt.patch" ) ) )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):

        # now do packaging with kdewin-packager
        self.doPackaging( "gpgme-qt", "20080115", True )

        return True
    
if __name__ == '__main__':
    subclass().execute()
