# -*- coding: utf-8 -*-
import base
import os
import utils
import info

from Source.GitSource import *
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ( '0.10.1', '0.10.2', '0.10.3', '0.10.4', '0.10.5', '0.10.6', '0.12.0' ):
            self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.gz' % i
            self.targetInstSrc[ i ] = 'poppler-%s' % i
        self.svnTargets['gitHEAD'] = "git://git.freedesktop.org/git/poppler/poppler"

        self.defaultTarget = "0.10.6"
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class Package(PackageBase, GitSource, CMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        GitSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        PackageBase.__init__(self)
        KDEWinPackager.__init__(self)
        
        self.subinfo.options.configure.defines = "-DBUILD_QT4_TESTS=ON"
        
if __name__ == '__main__':
    Package().execute()
