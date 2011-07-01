import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.6/kdenetwork'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdenetwork-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdenetwork-4.6.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs-bin/libidn'] = 'default'
        self.dependencies['win32libs-bin/libmsn'] = 'default'
        #mingw already contains libgmp
        if not compiler.isMinGW():
            self.dependencies['win32libs-bin/libgmp'] = 'default'
        self.shortDescription = "KDE Networking applications (Kopete, KGet)"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
