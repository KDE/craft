# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '1.8.0' ] = "ftp://ftp.gnu.org/gnu/gsasl/libgsasl-1.8.0.tar.gz"
        self.targetDigests['1.8.0'] = '08fd5dfdd3d88154cf06cb0759a732790c47b4f7'
        self.targetInstSrc[ '1.8.0' ] = "libgsasl-1.8.0"
        self.shortDescription = "GNU SASL is an implementation of the Simple Authentication and Security Layer framework and a few common SASL mechanisms"
        self.homepage = "http://www.gnu.org/software/gsasl"
        self.defaultTarget = '1.8.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-static --enable-shared "
        
        
