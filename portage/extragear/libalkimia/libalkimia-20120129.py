import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:alkimia'
        for ver in ['4.3.0', '4.3.1', '4.3.2']:
            self.targets[ ver ] = 'http://kde-apps.org/CONTENT/content-files/137323-libalkimia-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = "libalkimia-" + ver
        self.patchToApply['4.3.1'] = ("libalkimia-4.3.1-20110822.diff", 1)
        self.targetDigests['4.3.1'] = 'a8381bf4def252425aca31d0929e31b1aa82d0b5'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/mpir'] = 'default'
        self.shortDescription = "A library with common classes and functionality used by finance applications for the KDE SC."

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
