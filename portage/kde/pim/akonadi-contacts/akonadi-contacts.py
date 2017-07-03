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
        self.dependencies['kde/akonadi'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/ktextwidgets'] = 'default'
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.dependencies['kde/kcontacts'] = 'default'
        self.dependencies['kde/kmime'] = 'default'
        self.dependencies['kde/akonadi-mime'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


