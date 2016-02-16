# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies[ 'libs/qtbase' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = 'git://github.com/frankosterfeld/qtkeychain.git'
        for ver in ["0.4.0"]:
            self.targets[ ver ] = "https://github.com/frankosterfeld/qtkeychain/archive/v%s.tar.gz" % ver
            self.archiveNames[ ver ] = "qtkeychain-v%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = 'qtkeychain-%s' % ver
        self.targetDigests['0.4.0'] = '869ed20d15cc78ab3903701faf3100d639c3da57'
        self.defaultTarget = '0.4.0'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

