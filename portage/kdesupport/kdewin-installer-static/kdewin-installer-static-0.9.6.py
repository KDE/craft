import info
import os

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.svnTargets['amarokHEAD'] = 'trunk/kdesupport/kdewin-installer'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt-static'] = 'default'
        self.hardDependencies['dev-util/upx'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

        self.qtstatic = portage.getPackageInstance('libs','qt-static')
        self.qtstatic.setBuildTarget('4.5.2-patched')
        qmake = os.path.join(self.qtstatic.installDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.die("could not found qmake")
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines = "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s" \
            % qmake.replace('\\', '/')
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.options.configure.defines += " -DBUILD_FOR_AMAROK=ON"

if __name__ == '__main__':
    Package().execute()
