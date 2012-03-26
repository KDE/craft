# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/quassel/quassel.git'
        self.patchToApply[ 'gitHEAD' ] = ('cd_WINDOWS.diff', 1)
        self.svnTargets['0.6'] = 'git://gitorious.org/quassel/quassel.git|0.6|'
        for ver in ['0.7.1','0.7.2','0.7.3','0.8.0']:
            self.targets[ver] = 'http://quassel-irc.org/pub/quassel-%s.tar.bz2' % ver
            self.targetInstSrc[ver] = 'quassel-%s' % ver
        self.targetDigests['0.7.1'] = '791086da977033a1bbee3effa317668b3726bd7f'
        self.targetDigests['0.8.0'] = 'b74967fa9f19b5d7c708279075cc0ef3a3dbbe8b'
        
        self.defaultTarget = 'gitHEAD'


    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['dev-util/pkg-config'] = 'default'
        self.shortDescription = "a distributed IRC client"


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += " -DWITH_KDE=ON -DWITH_SYSLOG=OFF"



if __name__ == '__main__':
    Package().execute()
