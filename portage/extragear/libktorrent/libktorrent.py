import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libktorrent'
        for ver in ['1.3.1']:
            self.targets[ver] = "http://ktorrent.org/downloads/4." + ver[2:] + "/libktorrent-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "libktorrent-" + ver
            self.patchToApply[ver] = [("libktorrent-1.3.1-20130607.diff", 1)]
        self.patchToApply['gitHEAD'] = [("libktorrent-1.3.1-20130607.diff", 1)]

        self.shortDescription = "A BitTorrent protocol implementation."
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs/mpir'] = 'default'
        self.dependencies['win32libs/gpgme'] = 'default'
        self.dependencies['win32libs/gcrypt'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
