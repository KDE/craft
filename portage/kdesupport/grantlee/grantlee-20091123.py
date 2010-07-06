# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://gitorious.org/grantlee/grantlee.git"
        self.svnTargets['0.1'] = "git://gitorious.org/grantlee/grantlee.git|0.1"
        self.defaultTarget = '0.1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = '-DBUILD_TESTS=OFF'
        CMakePackageBase.__init__(self)
        
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            print("<%s>") % qmake
            utils.die("could not found qmake")
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += " -DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')
        
if __name__ == '__main__':
    Package().execute()
