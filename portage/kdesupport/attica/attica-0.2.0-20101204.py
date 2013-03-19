import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:attica'

        for ver in ['0.1.3','0.2.0', '0.4.1']:
            self.targets[ver] ='http://download.kde.org/stable/attica/attica-' + ver +'.tar.bz2'
            self.targetInstSrc[ver] = 'attica-' + ver
        self.shortDescription = "implements the Open Collaboration Services API"
        self.defaultTarget = 'gitHEAD'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
