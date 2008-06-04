import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.16'] = 'http://www.exiv2.org/exiv2-0.16.tar.gz'
        self.targetInstSrc['0.16'] = 'exiv2-0.16'
        self.defaultTarget = '0.16'
    
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
        self.system( "cd %s && patch -p0 < %s" % ( self.workdir, os.path.join( self.packagedir, "exiv2-cmake.diff" ) ) )
        return True
        
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

if __name__ == '__main__':
    subclass().execute()
