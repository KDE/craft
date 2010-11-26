import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kdesupport/qca'] = 'default' # okular/generators/ooo
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.dependencies['win32libs-bin/poppler'] = 'default'
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
