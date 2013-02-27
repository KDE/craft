import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'
        self.dependencies['libs/qt']            = 'default'
        self.dependencies['win32libs/librdf']   = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.buildDependencies['win32libs/clucene-core'] = 'default'
            self.dependencies['binary/virtuoso']             = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:soprano.git'

        for ver in ['2.9.0', '2.8.0']:
            self.svnTargets[ ver ] ='[git]kde:soprano.git||' + ver

        for ver in ['v2.8.0', 'v2.9.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/soprano/soprano-' + ver.replace('v', '') + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'soprano-' + ver[1:]
        self.patchToApply['v2.9.0'] = [("soprano-redland-callback.diff", 1)]
        self.shortDescription = "a RDF storage solutions library"
        self.defaultTarget = 'gitHEAD'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines="-DSOPRANO_DISABLE_SESAME2_BACKEND=YES -DSOPRANO_DISABLE_CLUCENE_INDEX=On "

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

if __name__ == '__main__':
    Package().execute()
