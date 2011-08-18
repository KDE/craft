import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libksane|KDE/4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.7." + ver + "/src/libksane-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'libksane-4.7.' + ver
        self.patchToApply['4.7.0'] = ("libksane-4.7.0-20110819.diff", 1)
        self.shortDescription = "libksane is an image scanning library that provides a QWidget that contains all the logic needed to interface a sacanner."
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
