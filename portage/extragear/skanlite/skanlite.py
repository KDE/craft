# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:skanlite.git'
        for ver in ['0.9', '1.0']:
            self.targets[ver] = "http://download.kde.org/stable/" + self.package + "/" + ver + "/src/" + self.package + "-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = self.package + '-' + ver
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'a small application for image scanning'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/libksane'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

