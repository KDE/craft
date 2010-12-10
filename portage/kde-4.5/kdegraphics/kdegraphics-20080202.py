import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdegraphics'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdegraphics-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdegraphics-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kdesupport/qca'] = 'default' # okular/generators/ooo
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['win32libs-bin/libspectre'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/chm'] = 'default'
        self.dependencies['win32libs-bin/djvu'] = 'default'
        self.dependencies['win32libs-bin/lcms'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
