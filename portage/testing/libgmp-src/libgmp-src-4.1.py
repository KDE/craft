import os
import sys
import base
import info
import utils
import shutil

class subinfo(info.infoclass):

    def setTargets( self ):
        self.targets['4.1'] = "http://www.cs.nyu.edu/exact/core/gmp/gmp-4.1.tar.gz"
        self.targetInstSrc['4.1'] = "gmp-4.1"
        self.defaultTarget = '4.1'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.buildType = "Release"

    def unpack( self ):    
        if( not base.baseclass.unpack( self ) ):
            return False
        # we have an own cmake script - copy it to the right place
        cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
        cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
        shutil.copy( cmake_script, cmake_dest )
        
        config_src = os.path.join( self.packagedir , "config.in" )
        config_dest = os.path.join( self.workdir, self.instsrcdir, "config.in" )
        shutil.copy( config_src, config_dest )

        fl  = os.path.join( self.workdir, self.instsrcdir, "mpn", "generic", "gmp-mparam.h")
        
        os.remove(fl)

        return True
        
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()
    
    def make_package( self ):
        self.instsrcdir = ""
        
if __name__ == '__main__':
    subclass().execute()
