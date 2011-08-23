import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.7/kdenetwork'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.7.' + ver + '/src/kdenetwork-4.7.' + ver + '.tar.bz2'
            self.targetInstSrc['4.7.' + ver] = 'kdenetwork-4.7.' + ver
        self.patchToApply['4.7.0'] = ("kdenetwork-4.7.0-20110824.diff", 1)
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
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
