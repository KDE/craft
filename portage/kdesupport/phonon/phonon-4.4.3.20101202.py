import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/automoc'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon.git'
        self.svnTargets['4.4'] = 'git://gitorious.org/phonon/phonon.git|4.4'
        self.patchToApply['gitHEAD'] = ("phonon-20100915.diff", 1)
        self.targets['4.4.3'] = 'http://download.kde.org/download.php?url=stable/phonon/4.4.3/phonon-4.4.3.tar.bz2'
        self.targetInstSrc['4.4.3'] = 'phonon-4.4.3'
        self.targetDigests['4.4.3'] = '50262d590beb648be9dcad6b913b920db19a84f8'
        self.patchToApply['4.4.3'] = ("phonon-20100915.diff", 1)
        self.defaultTarget = '4.4.3'
        
          
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF "
            
        if self.isTargetBuild():
            automoc = os.path.join(self.rootdir, "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                utils.warning("could not find automoc in <%s>" % automoc)
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += "-DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
