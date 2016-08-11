# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.dependencies[ 'libs/qtbase' ] = 'default'

    def setTargets( self ):
        self.svnTargets[ 'gitHEAD' ] = 'https://github.com/frankosterfeld/qtkeychain.git'
        for ver in ["0.4.0", "0.5.0", "0.7.0"]:
            self.targets[ ver ] = "https://github.com/frankosterfeld/qtkeychain/archive/v%s.tar.gz" % ver
            self.archiveNames[ ver ] = "qtkeychain-v%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = 'qtkeychain-%s' % ver
        self.targetDigests['0.4.0'] = '869ed20d15cc78ab3903701faf3100d639c3da57'
        self.targetDigests['0.5.0'] = (['e62d7ae9c8ae04784d8a5d0f213aaa22f1c02427e800ce88739e997f499bb514'], EmergeHash.HashAlgorithm.SHA256)
        self.targetDigests['0.7.0'] = (['9f9afaae8e909391d7fc932bac95e38befaac5b2eb49f6623a8efec60a2e6a3a'], EmergeHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.7.0'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

