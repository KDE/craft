import info
import emergePlatform
import utils
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
		# will be moved to kdewin-qt 
        self.dependencies['libs/qt'] = 'default'
		# will be moved to kdewin-tools
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/libpng'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.3.9'] = 'tags/kdewin32/0.3.9'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/kdewin'
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        # required for package generating because we build from svnHEAD by default
        self.subinfo.options.package.version = '0.5.4'
        self.subinfo.options.configure.defines = '-DBUILD_BASE_LIB_WITH_QT=ON -DBUILD_QT_LIB=ON '
        if not emergePlatform.isCrossCompilingEnabled() or self.isHostBuild():
            self.subinfo.options.configure.defines += ' -DBUILD_TOOLS=ON '
        if compiler.isMinGW_W32():
          self.subinfo.options.configure.defines += ' -DMINGW_W32=ON '
        CMakePackageBase.__init__( self )
        
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += " -DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')
			
    def make(self ):
        if self.isTargetBuild():
            os.environ["TARGET_INCLUDE"] = "%s;%s" % (os.path.join(self.mergeDestinationDir(), "include", "wcecompat"), os.getenv("TARGET_INCLUDE"))
        return CMakePackageBase.make( self )

if __name__ == '__main__':
    Package().execute()
