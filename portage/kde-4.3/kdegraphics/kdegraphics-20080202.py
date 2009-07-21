import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.3/kdegraphics'
        for ver in ['91', '95', '98']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.2.' + ver + '/src/kdegraphics-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdegraphics-4.2.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdegraphics-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdegraphics-4.3.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/qca'] = 'default' # okular/generators/ooo
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/poppler'] = 'default'
        self.hardDependencies['win32libs-bin/exiv2'] = 'default'
        self.hardDependencies['win32libs-bin/chm'] = 'default'
        self.hardDependencies['win32libs-bin/djvu'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
       return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdegraphics", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
