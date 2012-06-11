import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdemultimedia'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/kdemultimedia-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'kdemultimedia-4.8.0'
        for ver in ['1', '2', '3', '4']:
            self.targets['4.8.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.' + ver + '/src/kdemultimedia-4.8.' + ver + '.tar.xz'
            self.targetInstSrc['4.8.' + ver] = 'kdemultimedia-4.8.' + ver
        self.shortDescription = "KDE multimedia applications (jux, kmix, kmixctrl, kscd)"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs-bin/taglib'] = 'default'
        self.dependencies['win32libs-bin/libogg'] = 'default'
        self.dependencies['win32libs-bin/libvorbis'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
