import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkdcraw'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/libkdcraw-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'libkdcraw-4.8.0'
        for ver in ['4.8.1', '4.8.2', '4.8.3']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/libkdcraw-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = 'libkdcraw-' + ver
        
        for ver in ['4.8.0', '4.8.1', '4.8.2', '4.8.3']:
            self.patchToApply[ver] = [('libkdcraw-4.8.0-20120125.diff',1)]
        
        self.defaultTarget = '4.8.2'
        
        self.shortDescription = 'libkdcraw is a C++ interface around LibRaw library used to decode RAW picture files.'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
