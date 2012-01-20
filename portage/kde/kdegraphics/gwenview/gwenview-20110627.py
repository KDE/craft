
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:gwenview|KDE/4.8|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/gwenview-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'gwenview-4.8.' + ver
        self.patchToApply['4.8.0'] = [("replace-usage-of-unportable-mkdtemp-with-KTempDir-update.patch", 1)]
        self.shortDescription = "Image viewer for KDE"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-baseapps'] = 'default' # libkonq is needed
        self.dependencies['kde/libkipi'] = 'default' 
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'
   


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
