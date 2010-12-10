import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics#norecursive;trunk/KDE/kdegraphics/okular;;trunk/KDE/kdegraphics/cmake'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.dependencies['kde/kdegraphicslibs'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['win32libs-bin/chm'] = 'default'
        self.dependencies['win32libs-bin/djvu'] = 'default'

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.onlyBuildTargets = 'okular'
        self.subinfo.options.configure.defines = '-DBUILD_LIBS=Off'

if __name__ == '__main__':
    Package().execute()
