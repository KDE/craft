import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['win32libs-bin/chm'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default' # okular/generators/ooo
        self.dependencies['kde/kdelibs'] = 'default'
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['win32libs-bin/ebook-tools'] = 'default'
        self.dependencies['win32libs-bin/libspectre'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/djvu'] = 'default'
        self.dependencies['win32libs-bin/lcms'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
