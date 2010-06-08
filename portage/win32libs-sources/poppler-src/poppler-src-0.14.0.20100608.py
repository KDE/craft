# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ( '0.12.1', '0.12.2', '0.12.3', '0.12.4', '0.14.0' ):
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.gz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i
        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler|master"
        self.svnTargets['0.12-branch'] = "git://git.freedesktop.org/git/poppler/poppler|poppler-0.12"
        self.svnTargets['0.14-branch'] = "git://git.freedesktop.org/git/poppler/poppler|poppler-0.14"

        self.defaultTarget = "0.14.0"
    
    def setDependencies( self ):
        #self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        # does not work with mingw
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.hardDependencies['win32libs-bin/jpeg'] = 'default'
        self.hardDependencies['win32libs-bin/libpng'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
        self.subinfo.options.package.packageName = 'poppler'
        self.subinfo.options.configure.defines = "-DBUILD_QT4_TESTS=ON -DENABLE_XPDF_HEADERS=ON"
        
if __name__ == '__main__':
    Package().execute()
