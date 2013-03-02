import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qimageblitz'
        for ver in ['0.0.5','0.0.6']:
          self.targets[ver] ='http://download.kde.org/stable/qimageblitz/qimageblitz-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'qimageblitz-' + ver
        self.targets['20130212'] = "http://downloads.sourceforge.net/kde-windows/qimageblitz-20130212.tar.xz"
        self.targetInstSrc['20130212'] = "qimageblitz-20130212"
        self.shortDescription = "Graphical effects library for KDE4"
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
