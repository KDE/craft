# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:konversation|frameworks'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/karchive'] = 'default'
        self.dependencies['kde/kbookmarks'] = 'default'
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['kde/kconfigwidgets'] = 'default'
        self.dependencies['kde/kemoticons'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kidletime'] = 'default'
        self.dependencies['kde/knotifyconfig'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        self.dependencies['kde/kio'] = 'default'
        self.dependencies['kde/kparts'] = 'default'
        self.dependencies['kde/solid'] = 'default'
        self.dependencies['kde/sonnet'] = 'default'
        self.dependencies['kde/kwallet'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['qt-libs/phonon'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.shortDescription = "a KDE based irc client"

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

