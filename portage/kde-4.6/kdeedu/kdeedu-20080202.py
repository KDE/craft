import os
import sys
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.6/kdeedu'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdeedu-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdeedu-4.6.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.runtimeDependencies['kde-4.6/kde-runtime'] = 'default'
        self.dependencies['kde-4.6/kdelibs'] = 'default'
        self.dependencies['win32libs-bin/cfitsio'] = 'default'
        self.dependencies['win32libs-bin/libnova'] = 'default'
        self.dependencies['win32libs-bin/openbabel'] = 'default'
        self.shortDescription = "KDE education applications (KAlgebra, Marble, KStars)"


from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()
