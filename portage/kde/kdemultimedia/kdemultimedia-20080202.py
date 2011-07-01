import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.7/kdemultimedia'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.7.' + ver + '/src/kdemultimedia-4.7.' + ver + '.tar.bz2'
            self.targetInstSrc['4.7.' + ver] = 'kdemultimedia-4.7.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs-bin/taglib'] = 'default'
        self.dependencies['win32libs-bin/libogg'] = 'default'
        self.dependencies['win32libs-bin/libvorbis'] = 'default'
        self.shortDescription = "KDE multimedia applications (jux, kmix, kmixctrl, kscd)"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
