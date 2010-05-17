import info
import platform

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon.git'
        self.defaultTarget = 'gitHEAD'
        self.options.configure.defines = "-DPHONON_BUILD_EXAMPLES=OFF -DPHONON_BUILD_TESTS=OFF"
        if COMPILER == "mingw4":
            self.options.configure.defines +=" -DBUILD_PHONON_DS9=OFF"
          
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
        self.subinfo.options.configure.defines = ""
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            print("<%s>") % qmake
            utils.die("could not found qmake")
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')
            
        automoc = os.path.join(os.getenv( "KDEROOT" ), "lib", "automoc4", "Automoc4Config.cmake")
        if not os.path.exists(automoc):
            print("<%s>") % automoc
            utils.die("could not found automoc")
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += "-DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
            % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
