# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.6'] = 'ftp://ftp.gnupg.org/gcrypt/gnutls/gnutls-2.8.6.tar.bz2'
        self.targetInstSrc['2.8.6'] = 'gnutls-2.8.6'
        self.patchToApply['2.8.6'] = ('gnutls-2.8.6-20110118.diff', 1)
        self.defaultTarget = '2.8.6'

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'
        self.dependencies['win32libs/gcrypt'] = 'default'
        if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'

class PackageMinGW(AutoToolsBuildSystem):
    def __init__( self, **args ):
        AutoToolsBuildSystem.__init__(self)
        self.subinfo.options.configure.defines = "--disable-openpgp-authentication --disable-guile"

if compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__( self ):
            PackageMinGW.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            VirtualPackageBase.__init__( self )

