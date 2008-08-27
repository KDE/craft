import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['0.2.1'] = "http://libspectre.freedesktop.org/releases/libspectre-0.2.1.tar.gz"
        self.targetInstSrc['0.2.1'] = "libspectre-0.2.1"
        self.defaultTarget = '0.2.1'
    def setDependencies( self ):
        self.hardDependencies['testing/libgs'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.createCombinedPackage = True
        
    def unpack( self ):
        base.baseclass.unpack( self )
        self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "spectre-0.2.1-cmake.diff" ) ) )
        return True
        

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()
    
    def make_package( self ):
        self.instsrcdir = ""

        self.doPackaging( "spectre", os.path.basename(sys.argv[0]).replace("spectre-src-", "").replace(".py", ""), True )
        return True
  
if __name__ == '__main__':
    subclass().execute()
