# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler"
        for i in [ '0.38.0' ]:
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.xz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i
        self.patchToApply['0.38.0'] = ("poppler-0.38.0-20151130.diff", 1)
        self.targetDigests['0.38.0'] = '62d334116e509d59cd1d8f172f02c0a81e73182f'

        self.shortDescription = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = "0.38.0"

    def setDependencies( self ):
        self.dependencies['win32libs/win_iconv'] = 'default'
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/libjpeg-turbo'] = 'default'
        self.dependencies['win32libs/lcms'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libjpeg-turbo'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/libcurl'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.runtimeDependencies['data/poppler-data'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        self.subinfo.options.package.packageName = 'poppler'
        self.subinfo.options.configure.defines = "-DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON -DENABLE_UTILS=OFF"

