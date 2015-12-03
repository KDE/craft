import info
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.svnTargets['master'] = "[git]kde:okular|frameworks"
        self.shortDescription = "KDE document viewer"

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
        self.dependencies['kde/libkexiv2'] = 'default'
        self.dependencies['frameworks/kactivities'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kjs'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/threadweaver'] = 'default'
        self.dependencies['frameworks/kwallet'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

