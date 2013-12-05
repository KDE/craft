import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['libs/qttools'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:phonon'        
        self.shortDescription = "a Qt based multimedia framework"
        
        for ver in ['4.7.0']:
            self.targets[ver] = 'http://download.kde.org/stable/phonon/%s/phonon-%s.tar.xz' % (ver ,ver)
            self.targetInstSrc[ver] = 'phonon-%s' % ver
        
        self.targetDigests['4.7.0'] = 'feda28afe016fe38eb253f2be01973fc0226d10f'
        
        self.defaultTarget = '4.7.0'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON -DPHONON_BUILD_PHONON4QT5=ON"

        
if __name__ == '__main__':
    Package().execute()
