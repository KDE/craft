import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdegraphics'
        for ver in ['0', '1', '2']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdegraphics-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdegraphics-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-sources/poppler-src'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        if self.traditional:
            self.instdestdir = "kde"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
       return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdegraphics", self.buildTarget, True )
        else:
            return self.doPackaging( "kdegraphics", os.path.basename(sys.argv[0]).replace("kdegraphics-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
