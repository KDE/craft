import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkipi|KDE/4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.7." + ver + "/src/libkipi-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'libkipi-4.7.' + ver
        self.shortDescription = "Libkipi is an interface to use kipi-plugins from a KDE image management program like digiKam."
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
