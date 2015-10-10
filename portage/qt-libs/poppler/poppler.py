# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in [ '0.28.1', '0.35.0' ]:
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.xz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i

        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler|master"
        self.targetDigests['0.28.1'] = '017258af51cb556dc53af630c50165bb9fd76e4f'
        self.patchToApply['0.28.1'] =  ("poppler-0.28.1-20141204.diff",1)
        self.patchToApply['0.35.0'] =  ("poppler-0.35.0-20151007.diff",1)
        self.targetDigests['0.35.0'] = 'ad16c9674e7048ecd4e9225fc00f7ac07669e17d'

        self.shortDescription = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = "0.35.0"

    def setDependencies( self ):
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/openjpeg'] = 'default'
        self.dependencies['win32libs/lcms'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/jpeg'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/libcurl'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.runtimeDependencies['data/poppler-data'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        self.subinfo.options.package.packageName = 'poppler'
        self.subinfo.options.configure.defines = "-DBUILD_QT4_TESTS=ON -DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON"

