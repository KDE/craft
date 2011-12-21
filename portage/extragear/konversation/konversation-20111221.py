# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.2.1', '1.2.2', '1.2.3', '1.3', '1.3.1']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/' + ver + '/src/konversation-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'konversation-' + ver
        for ver in ['1.4']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/stable/konversation/' + ver + '/src/konversation-' + ver + '.tar.xz'
            self.targetInstSrc[ver] = 'konversation-' + ver
        self.patchToApply['1.3.1'] = ("konversation-1.3.1-20110822.diff", 1)
        self.svnTargets['gitHEAD'] = '[git]kde:konversation'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['virtual/kdepimlibs'] = 'default'
        self.shortDescription = "a KDE based irc client"

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
