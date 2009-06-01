# -*- coding: utf-8 -*-
import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.40'] = 'http://www.jedrea.com/chmlib/chmlib-0.40.tar.bz2'
        self.targetInstSrc['0.40'] = 'chmlib-0.40'
        self.defaultTarget = '0.40'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if not base.baseclass.unpack( self ):
            return False

        os.chdir( self.workdir )
        print os.path.join( self.workdir, self.instsrcdir )
        if self.buildTarget == '0.40':
            self.system( "cd %s && patch -p0 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "chm-cmake.diff" ) ) )
        
        return True
        
    def compile( self ):
        # building examples and debugging tools
        self.kdeCustomDefines = "-DBUILD_examples=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "chm", self.buildTarget, True )


if __name__ == '__main__':
    subclass().execute()
