import base
import utils
import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['2.0.0-beta2'] = 'http://prdownloads.sourceforge.net/krusader/krusader-2.0.0-beta2.tar.gz'
        self.targetInstSrc['2.0.0-beta2'] = 'krusader-2.0.0-beta2'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.instsrcdir = "krusader_kde4"
        
    def unpack( self ):
        print "krusader unpack called"
        # do the svn fetch/update
        if self.buildTarget == 'svnHEAD':
            repo = "http://krusader.svn.sourceforge.net/svnroot/krusader/trunk/krusader_kde4"
            self.svnFetch( repo )

            utils.cleanDirectory( self.workdir )
        else:
            if not base.baseclass.unpack( self ):
                return False

        return True

    def compile( self ):
        if self.subinfo.buildTarget == 'svnHEAD':
            self.kde.sourcePath = os.path.join( self.svndir, "krusader_kde4" )
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "krusader", os.path.basename(sys.argv[0]).replace("krusader-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
