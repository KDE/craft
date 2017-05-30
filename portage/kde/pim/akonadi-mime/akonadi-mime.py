# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Mime library"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['kde/akonadi'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['kde/kmime'] = 'default'
        self.dependencies['frameworks/kitemmodels'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['win32libs/shared-mime-info'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


