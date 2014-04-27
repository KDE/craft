# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ( '0.18.0', '0.18.1', '0.18.2', '0.20.3', '0.22.3' ):
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.gz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i
        for i in ( '0.24.3', '0.24.5' ):
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.xz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i
            
        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler|master"
        self.svnTargets['0.18-branch'] = "git://git.freedesktop.org/git/poppler/poppler|poppler-0.18"
        self.svnTargets['0.20-branch'] = "git://git.freedesktop.org/git/poppler/poppler|poppler-0.20"
        self.svnTargets['0.22-branch'] = "git://git.freedesktop.org/git/poppler/poppler|poppler-0.22"
        self.targetDigests['0.18.2'] = '7ef4eec20e849024c0cdd7a49c428d20eb3de875'
        self.targetDigests['0.22.3'] = '92fd3d2f56cf74bb76e4856a8ac606330343ba8d'
        self.targetDigests['0.24.3'] = '9aca24a8b012587ea579f72892863d9b3245009a'
        self.targetDigests['0.24.5'] = '7b7cabee85bd81a7e55c939740d5d7ccd7c0dda5'
        self.patchToApply["0.18.2"] = [("poppler-0.18.2-20130113.diff",1)]
        self.patchToApply["0.22.3"] = [("poppler-0.22.3-20130429.diff",1),
                                       ("poppler-0.22.3-20130615.diff",1)]
        self.patchToApply["0.24.3"] = [("poppler-0.24.3-20131110.diff",1)]
        self.patchToApply["0.24.5"] = [("poppler-0.24.5-20131110.diff",1)]

        self.shortDescription = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = "0.24.5"

    def setDependencies( self ):
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/openjpeg'] = 'default'
        self.dependencies['win32libs/lcms'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/jpeg'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/libcurl'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.runtimeDependencies['data/poppler-data'] = 'default'
        self.dependencies['libs/qt'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

        self.subinfo.options.package.packageName = 'poppler'
        self.subinfo.options.configure.defines = "-DBUILD_QT4_TESTS=ON -DENABLE_XPDF_HEADERS=ON -DENABLE_ZLIB=ON -DENABLE_LIBCURL=ON"

