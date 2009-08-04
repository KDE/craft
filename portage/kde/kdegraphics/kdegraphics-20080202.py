import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegraphics'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdegraphics-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdegraphics-4.0.' + ver
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/qca'] = 'default' # okular/generators/ooo
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-sources/poppler-src'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['win32libs-bin/tiff'] = 'default'
        self.hardDependencies['win32libs-bin/exiv2'] = 'default'
        self.hardDependencies['win32libs-bin/chm'] = 'default'
        self.hardDependencies['win32libs-bin/djvu'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
