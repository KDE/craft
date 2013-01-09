import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdemultimedia'
        self.shortDescription = "KDE multimedia applications (jux, kmix, kmixctrl, kscd)"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs/taglib'] = 'default'
        self.dependencies['win32libs/libogg'] = 'default'
        self.dependencies['win32libs/libvorbis'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
