# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies[ 'libs/qtbase' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]https://github.com/KDAB/KDReports.git'
        for ver in [ '1.7.1' ]:
            self.targets[ ver ] = 'https://github.com/KDAB/KDReports/archive/kdreports-1.7.1.tar.gz'
            self.targetInstSrc[ ver ] = "kdreports-%s" % ver
            self.archiveNames[ ver ] = "kdreports-%s.tar.gz" % ver
        self.targetDigests['1.7.1'] = (['d75f4bf3399bea51837b7a931be8640823168ba19d6dfd346db3e2270a26ca23'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '1.7.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

