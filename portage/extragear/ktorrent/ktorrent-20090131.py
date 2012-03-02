import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:ktorrent'
        for version in ['3.2beta1', '3.2rc1', '3.2', '3.2.2', '3.2.3', '3.3beta1']:
            self.targets[version] = 'http://ktorrent.org/downloads/' + version + '/ktorrent-' + version + '.tar.bz2'
            self.targetInstSrc[version] = 'ktorrent-' + version
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['virtual/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs-bin/mpir'] = 'default'
        self.dependencies['extragear/libktorrent'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
