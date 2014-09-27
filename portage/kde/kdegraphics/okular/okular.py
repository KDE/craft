import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:okular|frameworks'
        self.shortDescription = 'Framework to build IDE-like applications'
        self.shortDescription = "KDE document viewer"
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.buildDependencies['win32libs/chm'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['qt-libs/poppler'] = 'default'
        self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.dependencies['win32libs/djvu'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/ebook-tools'] = 'default'
        self.buildDependencies['win32libs/libspectre'] = 'default'
        self.dependencies['binary/ghostscript'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['frameworks/kactivities'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

