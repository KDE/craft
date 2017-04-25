import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.patchToApply["5.33.0"] = [("0007-fix-duplicated-symbols-compilation-error-with-mingw-.patch", 1)]

        self.shortDescription = "A file metadata and text extraction library"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        
        self.dependencies["frameworks/karchive"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        
        # self.dependencies['qt-libs/poppler'] = 'default'
        self.dependencies['win32libs/taglib'] = 'default'
        self.dependencies['win32libs/exiv2'] = 'default'
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

