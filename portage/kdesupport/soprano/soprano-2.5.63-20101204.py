import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base']            = 'default'
        self.dependencies['libs/qt']                 = 'default'
        self.dependencies['win32libs-bin/librdf']   = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.buildDependencies['win32libs-bin/clucene-core'] = 'default'
            self.dependencies['testing/virtuoso']   = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/soprano'
        self.svnTargets['gitHEAD'] = '[git]kde:soprano.git'

        for ver in ['2.5.63', '2.6.0', '2.6.0', '2.0.0', '2.0.1', '2.0.2',
                    '2.0.3', '2.0.99', '2.1', '2.1.1', '2.1.64', '2.1.65',
                    '2.1.67', '2.2', '2.2.1', '2.2.2']:
            self.svnTargets[ver] ='[git]kde:soprano.git||' + ver
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/soprano'
        for i in ['4.4.0', '4.4.1', '4.4.2', '4.4.3', '4.4.4', '4.4']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.4/soprano'
        self.shortDescription = "a RDF storage solutions library"
        # 2.6.0 is the last version needing raptor 1 to update to a later version
        # you need also to update librdf librasqual and libraptor2
        self.defaultTarget = '2.6.0'

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
