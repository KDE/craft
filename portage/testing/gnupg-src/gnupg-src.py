# -*- coding: utf-8 -*-
import info

from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.10'] = 'ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-1.4.10.tar.bz2'
        self.targetInstSrc['1.4.10'] = 'gnupg-1.4.10'
        self.targetDigests['1.4.10'] = 'fd1b6a5f3b2dd836b598a1123ac257b8f105615d'
        self.defaultTarget = '1.4.10'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__(self)
        self.buildInSource = True

