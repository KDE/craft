import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdeplasma-addons|4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "http://download.kde.org/stable/4.7." + ver + "/src/kdeplasma-addons-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'kdeplasma-addons-4.7.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kde-workspace'] = 'default'
        self.shortDescription = "All kind of addons to improve your Plasma experience"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
