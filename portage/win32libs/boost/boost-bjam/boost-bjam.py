from CraftDebug import craftDebug
import info
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc = self.package.replace("boost-","").replace("-", "_") )

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.runtimeDependencies['virtual/base'] = 'default'
        self.runtimeDependencies['win32libs/boost-headers'] = 'default'


from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def install(self):
        if OsUtils.isUnix():
            return utils.copyFile( os.path.join(portage.PortageInstance.getPackageInstance('win32libs', 'boost-headers').sourceDir(),"tools","build", "bjam" ),
                                os.path.join( self.imageDir(), "bin", "bjam" ) )
        else:
            return utils.copyFile( os.path.join(portage.PortageInstance.getPackageInstance('win32libs', 'boost-headers').sourceDir(),"tools","build", "bjam.exe" ),
                                   os.path.join( self.imageDir(), "bin", "bjam.exe" ) )


    def make(self):
        if OsUtils.isUnix():
            cmd = "./bootstrap.sh  --with-toolset="
            if craftCompiler.isClang():
                cmd += "clang"
            elif craftCompiler.isGCC():
                cmd += "gcc"
        else:
            cmd = "bootstrap.bat "
            if craftCompiler.isClang():
                cmd += "clang"
            elif craftCompiler.isMinGW():
                cmd += "mingw"
            elif craftCompiler.isMSVC():
                platform = str(craftCompiler.getMsvcPlatformToolset())
                cmd += f"vc{platform[:2]}"
        utils.system(cmd, cwd = os.path.join(portage.PortageInstance.getPackageInstance('win32libs',
                'boost-headers').sourceDir(),"tools","build")) or craftDebug.log.critical(
                "command: %s failed" % (cmd))
        return True


