# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:konversation|frameworks'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kemoticons'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kidletime'] = 'default'
        self.dependencies['frameworks/knotifyconfig'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
        self.dependencies['frameworks/sonnet'] = 'default'
        self.dependencies['frameworks/kwallet'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['qt-libs/phonon'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.shortDescription = "a KDE based irc client"

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

