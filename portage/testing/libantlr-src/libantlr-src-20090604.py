# -*- coding: utf-8 -*-
import base
import utils
import os
import shutil
import info

# this is just the C runtime but we nevertheless use the library name for it

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.1.3'] = 'http://www.antlr.org/download/C/libantlr3c-3.1.3.tar.gz'
        self.targetInstSrc['3.1.3'] = 'libantlr3c-3.1.3'
        self.defaultTarget = '3.1.3'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if not base.baseclass.unpack( self ):
            return False

        cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
        cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
        shutil.copy( cmake_script, cmake_dest )
        
        return True
        
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "libantlr", self.buildTarget, True )


if __name__ == '__main__':
    subclass().execute()
