import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        for ver in ['0.0.5','0.0.6']:
          self.targets[ver] ='http://download.kde.org/download.php?url=stable/qimageblitz/qimageblitz-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'qimageblitz-' + ver 
          
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/qimageblitz'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/qimageblitz'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
