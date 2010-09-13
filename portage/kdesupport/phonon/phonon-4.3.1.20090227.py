import info
import platform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon.git'
        self.svnTargets['4.4'] = 'git://gitorious.org/phonon/phonon.git|4.4'
        self.defaultTarget = 'gitHEAD'
        
        self.options.configure.defines = "-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF"
        if COMPILER == "mingw4":
            self.options.configure.defines +=" -DBUILD_PHONON_DS9=OFF "
          
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
            
        if self.isTargetBuild():
            automoc = os.path.join(self.rootdir, "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                print("<%s>") % automoc
                utils.die("could not found automoc")
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += "-DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
