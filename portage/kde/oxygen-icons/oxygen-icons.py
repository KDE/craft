import info
import kdedefaults as kd
from EmergeConfig import *

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

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        # this package could be used for all build types (only images)
        ## \todo find a way to reuse this build output for different build types
        CMakePackageBase.__init__( self )
        self.subinfo.options.useBuildType = False
        self.subinfo.options.useCompilerType = False



