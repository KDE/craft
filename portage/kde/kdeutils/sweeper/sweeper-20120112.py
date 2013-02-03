import info
from os.path import dirname as dn, join as j

class subinfo(info.infoclass):
    def setTargets( self ):
        kdepath = j(dn(__file__), '..', '..')
        kdebranch = open(j(kdepath, 'kdebranch')).read()
        kdeversion = open(j(kdepath, 'kdeversion')).read() + '.'
        package = 'sweeper'

        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (package, kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kdeversion + ver] = "ftp://ftp.kde.org/pub/kde/stable/" + kdeversion + ver + "/src/" + package + "-" + kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kdeversion + ver] = package + '-' + kdeversion + ver

        self.shortDescription = "a tool to clean unwanted traces"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
