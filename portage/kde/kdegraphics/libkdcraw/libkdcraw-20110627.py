import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkdcraw|KDE/4.8|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/libkdcraw-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'libkdcraw-4.8.' + ver
        self.patchToApply['4.8.0'] = [("libkdcraw-4.8.0-20120125.diff", 1)]
        self.shortDescription = "libkdcraw is a C++ interface around LibRaw library used to decode RAW picture files."
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
