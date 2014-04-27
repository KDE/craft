# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.14.21' ] = "http://ftp.gnome.org/pub/gnome/sources/libgsf/1.14/libgsf-1.14.21.tar.bz2"
        self.targetInstSrc[ '1.14.21' ] = "libgsf-1.14.21"
        self.targetDigests['1.14.21'] = '17981f238f1f8dddb7af01c161bd6a1c4d5e85d2'
        self.patchToApply['1.14.21'] = [("libgsf-1.14.21-20110725.diff", 1)]
        self.shortDescription = "an I/O abstraction for reading/writing compound files"
        self.defaultTarget = '1.14.21'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['testing/glib-src'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/libbzip2'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

