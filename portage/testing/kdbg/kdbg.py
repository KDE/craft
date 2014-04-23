# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://repo.or.cz/kdbg.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'


class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
