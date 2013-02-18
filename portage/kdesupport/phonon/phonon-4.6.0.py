import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/automoc'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:phonon'
        for ver in ['4.4.3', '4.4.4', '4.5.0']:
            self.targets[ver] = 'http://download.kde.org/stable/phonon/%s/src/phonon-%s.tar.bz2' % (ver ,ver)
            self.targetInstSrc[ver] = 'phonon-%s' % ver
        for ver in ['4.5.1','4.6.0']:
            self.targets[ver] = 'http://download.kde.org/stable/phonon/%s/src/phonon-%s.tar.xz' % (ver ,ver)
            self.targetInstSrc[ver] = 'phonon-%s' % ver
        if ver in ['4.4.3', '4.4.4']: self.patchToApply[ver] = ("phonon-20100915.diff", 1)
        self.patchToApply['4.5.1'] = ("phonon-fix-gcc-4.5.diff", 1)
        self.patchToApply['4.6.0'] = ("phonon-4.6.0-fix-gcc-4.5.diff", 1)
        self.targetDigests['4.4.3'] = '50262d590beb648be9dcad6b913b920db19a84f8'
        self.targetDigests['4.4.4'] = '7f31752c20efecbe63c7b312ceb28819fa337943'
        self.targetDigests['4.5.0'] = '122f7c53939a2c40c3312c2f5e59f25ca2c9ee53'
        self.targetDigests['4.6.0'] = 'd8dbc188b58c6dd9c6a73d3742a25291e647bb95'


        
        self.shortDescription = "a Qt based multimedia framework"
        self.defaultTarget = '4.6.0'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON"

        if self.isTargetBuild():
            automoc = os.path.join(self.rootdir, "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                utils.warning("could not find automoc in <%s>" % automoc)
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += " -DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')
        else:
            automoc = os.path.join(self.mergeDestinationDir(), "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                utils.warning("could not find automoc in <%s>" % automoc)
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += " -DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')
        
if __name__ == '__main__':
    Package().execute()
