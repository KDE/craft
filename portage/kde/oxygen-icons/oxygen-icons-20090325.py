import info
import kdedefaults as kd

class subinfo(info.infoclass):

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/oxygen-icons'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
            self.targetDigestUrls[ kd.kdeversion + ver  ] = 'http://download.kde.org/stable/' + kd.kdeversion + ver + '/src/' + self.package + '-' + kd.kdeversion + ver + '.tar.xz.sha1'

        self.shortDescription = "icons and bitmaps for the oxygen style"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        # this package could be used for all build types (only images)
        ## \todo find a way to reuse this build output for different build types
        self.subinfo.options.useBuildType = False
        self.subinfo.options.useCompilerType = False
        CMakePackageBase.__init__( self )

    def qmerge( self ):
        ''' When crosscompiling install oxygen files
            also into the targets directory '''
        ret = CMakePackageBase.qmerge(self)
        if emergePlatform.isCrossCompilingEnabled():
            utils.copyDir(self.imageDir(),
                    os.path.join(self.rootdir,
                    os.environ["EMERGE_TARGET_PLATFORM"]))
        return ret


if __name__ == '__main__':
    Package().execute()
