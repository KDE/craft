# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Contacts library"
        self.patchToApply['17.04.0'] = [("akonadi-contacts-17.04.0-fix-compile.diff", 1)]
        self.patchToApply['17.04.1'] = [("akonadi-contacts-17.04.1-fix-compile.diff", 1)]
        self.patchToApply['17.04.2'] = [("akonadi-contacts-17.04.1-fix-compile.diff", 1)]


    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['libs/qtwebengine'] = 'default'
        self.runtimeDependencies['kde/akonadi'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/ktextwidgets'] = 'default'
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies['kde/kcontacts'] = 'default'
        self.runtimeDependencies['kde/kmime'] = 'default'
        self.runtimeDependencies['kde/akonadi-mime'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


