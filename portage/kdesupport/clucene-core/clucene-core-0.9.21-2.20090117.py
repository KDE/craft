import base
import utils
import shutil
import os
import sys
import info

class subinfo (info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['0.9.16a'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.16a.tar.bz2"
        self.targetInstSrc['0.9.16a'] = os.path.join( "clucene-core-0.9.16a", "src" )
        self.targets['0.9.20'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.20.tar.bz2"
        self.targetInstSrc['0.9.20'] = os.path.join( "clucene-core-0.9.20", "src" )
        self.targets['0.9.21b'] = "http://downloads.sourceforge.net/sourceforge/clucene/clucene-core-0.9.21b.tar.bz2"
        self.targetInstSrc['0.9.21b'] = os.path.join( "clucene-core-0.9.21b", "src" )
        self.defaultTarget = '0.9.21b'


class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return True

        # we have an own cmake script - copy it to the right place
        mydir = os.path.join( self.workdir, self.instsrcdir )
        cmake_script = ""
        if self.buildTarget == '0.9.16a':
            cmake_script = os.path.join( self.packagedir , "CMakeLists-0.9.16.txt" )
        else:
            cmake_script = os.path.join( self.packagedir , "CMakeLists-0.9.20.txt" )
        cmake_dest = os.path.join( mydir, "CMakeLists.txt" )
        shutil.copy( cmake_script, cmake_dest )
        cmake_script = os.path.join( self.packagedir , "clucene-config.h.cmake" )
        cmake_dest = os.path.join( mydir, "Clucene", "clucene-config.h.cmake" )
        shutil.copy( cmake_script, cmake_dest )

        return True

    def compile( self ):
        self.kdeCustomDefines="-DCLUCENE_VERSION:STRING="+self.buildTarget
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "clucene-core", self.buildTarget, True )

    
if __name__ == '__main__':
    subclass().execute()
