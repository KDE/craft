import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        for ver in ['0.0.5','0.0.6']:
          self.targets[ver] ='http://download.kde.org/download.php?url=stable/qimageblitz/qimageblitz-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'qimageblitz-' + ver
        for ver in ['20130212']:
          self.targets[ver] ='http://downloads.sourceforge.net/kde-windows/qimageblitz-' + ver + '.tar.xz'
          self.targetInstSrc[ver] = 'qimageblitz-' + ver

        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/qimageblitz'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/qimageblitz'
        self.shortDescription = "Graphical effects library for KDE4"
        self.defaultTarget = '20130212'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


