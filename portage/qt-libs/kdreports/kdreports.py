# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies[ 'libs/qtbase' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = '[git]https://github.com/KDAB/KDReports.git'
        for ver in [ '1.7.1' ]:
            self.targets[ '1.7.1' ] = 'https://github.com/KDAB/KDReports/releases/download/kdreports-1.7.1/kdreports-1.7.1.zip'
            self.targetInstSrc['1.7.1'] = "kdreports-%s" % ver

        self.defaultTarget = '1.7.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

