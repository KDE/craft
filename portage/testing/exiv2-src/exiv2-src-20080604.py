import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.16'] = 'http://www.exiv2.org/exiv2-0.16.tar.gz'
        self.targetInstSrc['0.16'] = 'exiv2-0.16'
        self.targets['0.17'] = 'http://www.exiv2.org/exiv2-0.17.tar.gz'
        self.targetInstSrc['0.17'] = 'exiv2-0.17'
        self.svnTargets['svnHEAD'] = 'unstable'
        self.defaultTarget = '0.17'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        if self.subinfo.buildTarget == 'svnHEAD':
            self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )

    def unpack( self ):
        if not self.buildTarget == 'svnHEAD':
            if not base.baseclass.unpack( self ):
                return False
        else:
            repo = 'svn://dev.robotbattle.com/exiv2/branches/'
            if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
                self.svnFetch( repo + self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
            else:
                return False
            utils.cleanDirectory( self.workdir )
        

        os.chdir( self.workdir )
        if self.buildTarget == '0.16':
            self.system( "cd %s && patch -p0 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "exiv2-cmake.diff" ) ) )
        elif self.buildTarget == '0.17':
            self.system( "cd %s && patch -p0 < %s" % ( os.path.join( self.workdir, self.instsrcdir ), os.path.join( self.packagedir, "exiv2-0.17-cmake.diff" ) ) )
        
        return True
        
    def compile( self ):
        if self.subinfo.buildTarget == 'svnHEAD':
            self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.subinfo.buildTarget == 'svnHEAD':
            self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
        self.doPackaging( "exiv2", "0.18svn-0", True )


if __name__ == '__main__':
    subclass().execute()
