import info
import emergePlatform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/automoc'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:phonon'
        for ver in ['4.7.0','4.7.1']:
            self.targets[ver] = 'http://download.kde.org/stable/phonon/%s/phonon-%s.tar.xz' % (ver ,ver)
            self.targetInstSrc[ver] = 'phonon-%s' % ver
        self.patchToApply['4.7.0'] = ("phonon-4.7.0-fix-dll-linkage.diff", 1) # upstream
        self.targetDigests['4.7.0'] = 'feda28afe016fe38eb253f2be01973fc0226d10f'
        self.targetDigests['4.7.1'] = 'f1d3214a752d97028dc4ed910a832c1272951522'

        self.shortDescription = "a Qt based multimedia framework"
        self.defaultTarget = '4.7.1'


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
