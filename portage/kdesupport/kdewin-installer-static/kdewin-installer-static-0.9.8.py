import info
import os

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdewin-installer'
        self.defaultTarget = 'gitHEAD'
        self.svnTargets['amarokHEAD'] = '[git]kde:kdewin-installer'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['libs/qt-static-src'] = 'default'
        self.buildDependencies['dev-util/upx'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.noDefaultInclude = True
        self.subinfo.options.configure.noDefaultLib = True

        self.qtstatic = portage.getPackageInstance('libs','qt-static-src')
        self.qtstatic.setBuildTarget('4.7.4')
        qmake = os.path.join(self.qtstatic.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines = "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s" \
            % qmake.replace('\\', '/')
        if self.buildTarget == 'amarokHEAD':
            self.subinfo.options.configure.defines += " -DBUILD_FOR_AMAROK=ON"

if __name__ == '__main__':
    Package().execute()
