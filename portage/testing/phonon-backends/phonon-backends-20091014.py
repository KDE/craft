# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/playground/multimedia/phonon-backends"
        self.defaultTarget = 'svnHEAD'
        self.options.configure.defines = "-DWITH_VLC=OFF"

    def setDependencies( self ):
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['testing/mplayer'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
