# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Console Tools"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kitemmodels'] = 'default'
        self.dependencies['frameworks/ktextwidgets'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/kcrash'] = 'default'
        self.dependencies['kde/kpimtextedit'] = 'default'
        self.dependencies['kde/akonadi'] = 'default'
        self.dependencies['kde/kcontats'] = 'default'
        self.dependencies['kde/akonadi-contacts'] = 'default'
        self.dependencies['kde/kcalcore'] = 'default'
        self.dependencies['kde/calendarsupport'] = 'default'
        self.dependencies['kde/akonadi-mime'] = 'default'
        self.dependencies['kde/kimap'] = 'default'
        self.dependencies['kde/messagelib'] = 'default'
        self.dependencies['kde/kmime'] = 'default'
        self.dependencies['kde/libkleo'] = 'default'
        self.dependencies['kde/libkdepim'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if not self.subinfo.options.isActive("binary/mysql"):
            self.subinfo.options.configure.defines += " -DDATABASE_BACKEND=SQLITE "


