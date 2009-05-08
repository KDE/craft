import base
import utils
import os
import shutil
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for f in ( '16', '17', '18', '18.1' ):
          ver = '0.' + f
          self.targets[ver]       = 'http://www.exiv2.org/exiv2-%s.tar.gz' % ver
          self.targetInstSrc[ver] = 'exiv2-%s' % ver
          self.patchToApply[ver]  = ( 'exiv2-%s-cmake.diff' % ver, 0 )

        self.svnTargets['svnHEAD'] = 'unstable'
        self.defaultTarget = '0.18.1'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/iconv']   = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/expat']   = 'default'
        self.hardDependencies['win32libs-bin/zlib']    = 'default'
        self.hardDependencies['virtual/base']          = 'default'
        
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
            return self.doPackaging( "exiv2", "0.18svn-0", True )
        else:
            return self.doPackaging( "exiv2", self.subinfo.buildTarget, True)


if __name__ == '__main__':
    subclass().execute()
