# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Akonadi Console Tools"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/kcompletion'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kitemmodels'] = 'default'
        self.runtimeDependencies['frameworks/ktextwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/kcrash'] = 'default'
        self.runtimeDependencies['kde/kpimtextedit'] = 'default'
        self.runtimeDependencies['kde/akonadi'] = 'default'
        self.runtimeDependencies['kde/kcontacts'] = 'default'
        self.runtimeDependencies['kde/akonadi-contacts'] = 'default'
        self.runtimeDependencies['kde/kcalcore'] = 'default'
        self.runtimeDependencies['kde/calendarsupport'] = 'default'
        self.runtimeDependencies['kde/akonadi-mime'] = 'default'
        self.runtimeDependencies['kde/kimap'] = 'default'
        self.runtimeDependencies['kde/messagelib'] = 'default'
        self.runtimeDependencies['kde/kmime'] = 'default'
        self.runtimeDependencies['kde/libkleo'] = 'default'
        self.runtimeDependencies['kde/libkdepim'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if not self.subinfo.options.isActive("binary/mysql"):
            self.subinfo.options.configure.defines += " -DDATABASE_BACKEND=SQLITE "


