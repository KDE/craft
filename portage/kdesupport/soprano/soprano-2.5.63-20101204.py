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

        for ver in ['2.8.0', '2.9.0', '2.9.2', '2.9.3', '2.9.4']:
            self.svnTargets[ ver ] ='[git]kde:soprano.git||v' + ver
            self.targets[ 'v' + ver ] = 'http://downloads.sourceforge.net/soprano/soprano-' + ver + '.tar.bz2'
            self.targetInstSrc[ 'v' + ver ] = 'soprano-' + ver
        self.patchToApply['v2.9.0'] = [("soprano-redland-callback.diff", 1),
                                       ("0001-test-if-virtuoso-executable-exists-first.patch", 1),
                                       ("0002-use-QLocalSocket-on-Windows-since-this-is-what-the-o.patch", 1)]
        self.patchToApply['2.9.0'] = self.patchToApply['v2.9.0']
        self.patchToApply['v2.9.2'] = [("soprano-redland-callback.diff", 1),
                                       ("0001-test-if-virtuoso-executable-exists-first.patch", 1),
                                       ("0002-use-QLocalSocket-on-Windows-since-this-is-what-the-o.patch", 1)]
        self.patchToApply['2.9.2'] = self.patchToApply['v2.9.2']
        self.targetDigests['v2.9.3'] = '9137c21e31c802ac9c45564962e07017952cb9c5'
        self.patchToApply['v2.9.3'] = [("soprano-redland-callback.diff", 1),
                                       ("0001-test-if-virtuoso-executable-exists-first.patch", 1),
                                       ("0002-use-QLocalSocket-on-Windows-since-this-is-what-the-o.patch", 1)]
        self.patchToApply['2.9.3'] = self.patchToApply['v2.9.3']
        self.targetDigests['v2.9.4'] = '97bd76df4a9f9336358dd9d7175c72b84d4ec6a0'
        self.patchToApply['v2.9.4'] = [("0001-test-if-virtuoso-executable-exists-first.patch", 1),
                                       ("0002-use-QLocalSocket-on-Windows-since-this-is-what-the-o.patch", 1)]
        self.patchToApply['2.9.4'] = self.patchToApply['v2.9.4']

        self.shortDescription = "a RDF storage solutions library"
        self.defaultTarget = 'v2.9.4'

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
