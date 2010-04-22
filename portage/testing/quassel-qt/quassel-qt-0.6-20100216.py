# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/quassel/quassel.git'
        self.targetMergePath['gitHEAD'] = "bin";
        self.svnTargets['0.6'] = 'git://gitorious.org/quassel/quassel.git|0.6|'
        self.targetMergePath['0.6'] = "bin";
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
     

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += " -DWITH_DBUS=OFF "

      


if __name__ == '__main__':
    Package().execute()
