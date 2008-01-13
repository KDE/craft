import base
import utils
import shutil
import os
import sys
import info

SRC_URI= """
http://garr.dl.sourceforge.net/sourceforge/clucene/clucene-core-0.9.16a.tar.bz2
"""

class subinfo (info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        #self.targets['0.9.16a'] = "http://garr.dl.sourceforge.net/sourceforge/clucene/clucene-core-0.9.16a.tar.bz2"
        self.svnTargets['svnHEAD'] = False
        #self.defaultTarget = '0.9.16a'
        self.defaultTarget = 'svnHEAD'


class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, SRC_URI )
        self.instsrcdir = os.path.join( "clucene-core-0.9.16a", "src" )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return True

        # we have an own cmake script - copy it to the right place
        mydir = os.path.join( self.workdir, self.instsrcdir )
        cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
        cmake_dest = os.path.join( mydir, "CMakeLists.txt" )
        shutil.copy( cmake_script, cmake_dest )
        cmake_script = os.path.join( self.packagedir , "clucene-config.h.cmake" )
        cmake_dest = os.path.join( mydir, "Clucene", "clucene-config.h.cmake" )
        shutil.copy( cmake_script, cmake_dest )

        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # FIXME?
        if self.traditional:
            self.instdestdir = "kde"
            self.instsrcdir = "clucene"
            return self.doPackaging( "clucene", "0.9.16a-1", True )
        else:
            self.instsrcdir = "clucene-core-0.9.16a"
            return self.doPackaging( "clucene-core", os.path.basename(sys.argv[0]).replace("clucene-core-", "").replace(".py", ""), True )

    
if __name__ == '__main__':
    subclass().execute()
