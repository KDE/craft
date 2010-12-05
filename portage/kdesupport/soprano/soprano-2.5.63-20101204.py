import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base']            = 'default'
        self.dependencies['libs/qt']                 = 'default'
        self.dependencies['win32libs-bin/redland']   = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.buildDependencies['win32libs-bin/clucene-core'] = 'default'
            self.dependencies['testing/virtuoso']   = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/soprano'
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/soprano.git'
        
        for ver in ['2.5.63']:
          self.targets[ver] ='http://downloads.sourceforge.net/sourceforge/Soprano/soprano-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'soprano-' + ver
          
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/soprano'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/soprano'
        self.defaultTarget = 'gitHEAD'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines="-DSOPRANO_DISABLE_SESAME2_BACKEND=YES "
            
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

if __name__ == '__main__':
    Package().execute()
