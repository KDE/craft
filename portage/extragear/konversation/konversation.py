# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['1.7'] = '[git]kde:konversation|1.7'
        self.svnTargets['master'] = '[git]kde:konversation|master'
        self.defaultTarget = '1.7'

    def setDependencies(self):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kbookmarks'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kemoticons'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kidletime'] = 'default'
        self.runtimeDependencies['frameworks/knotifyconfig'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kparts'] = 'default'
        self.runtimeDependencies['frameworks/solid'] = 'default'
        self.runtimeDependencies['frameworks/sonnet'] = 'default'
        self.runtimeDependencies['frameworks/kwallet'] = 'default'
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['qt-libs/phonon'] = 'default'
        self.shortDescription = "a KDE based irc client"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "Konversation"
        self.defines["executable"] = "bin\\konversation.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "konversation.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
