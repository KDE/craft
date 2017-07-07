# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Search Agent"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['win32libs/xapian-core'] = 'default'
        self.runtimeDependencies['kde/akonadi'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kcrash'] = 'default'
        self.runtimeDependencies['frameworks/kcmutils'] = 'default'
        self.runtimeDependencies['kde/akonadi-mime'] = 'default'
        self.runtimeDependencies['kde/kmime'] = 'default'
        self.runtimeDependencies['kde/kcalcore'] = 'default'
        self.runtimeDependencies['kde/kcontacts'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


