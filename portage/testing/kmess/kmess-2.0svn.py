import base
import utils
import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.instsrcdir = "kmess"
        
    def unpack( self ):
        print "kmess unpack called"
        # do the svn fetch/update
        repo = "http://kmess.svn.sourceforge.net/svnroot/kmess/trunk/kmess"
        self.svnFetch( repo )

        utils.cleanDirectory( self.workdir )

        # now copy the tree below destdir/trunk to workdir
        srcdir = os.path.join( self.svndir, "kmess" )
        destdir = os.path.join( self.workdir, "kmess" )
        utils.copySrcDirToDestDir( srcdir, destdir )

        os.chdir( destdir )

        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kmess", os.path.basename(sys.argv[0]).replace("kmess-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
