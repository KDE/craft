import base
import utils
import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = False
        self.targets['1.0'] = 'http://bilbo.gnufolks.org/packages/bilbo-1.0-src.tar.gz'
        self.targetInstSrc['1.0'] = 'bilbo'
        self.defaultTarget = '1.0'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
        
class subclass( base.baseclass ):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.instsrcdir = "bilboblogger"
        
    def unpack( self ):
        print "BilboBlogger unpack called"
        # do the svn fetch/update
        if not base.baseclass.unpack( self ):
            return False

        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "bilboblogger", os.path.basename(sys.argv[0]).replace("bilbo-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
