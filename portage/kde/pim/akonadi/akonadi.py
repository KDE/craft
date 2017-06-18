# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["17.04.0"] = [("akonadi-17.04.0-20170530.diff", 1)]

        self.shortDescription = "A storage service for PIM data and meta data"

    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/shared-mime-info'] = 'default'
        self.dependencies['frameworks/kdesignerplugin'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if not self.subinfo.options.isActive("binary/mysql"):
            self.subinfo.options.configure.defines += " -DDATABASE_BACKEND=SQLITE "


