from CraftDebug import craftDebug
import info
from CraftOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc = self.package.replace("boost-","").replace("-", "_") )

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/boost-headers'] = 'default'


from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def install(self):
        if OsUtils.isUnix():        
            return utils.copyFile( os.path.join(portage.getPackageInstance('win32libs', 'boost-headers').sourceDir(),"tools","build", "bjam" ),
                                os.path.join( self.imageDir(), "bin", "bjam" ) )
        else:
            return utils.copyFile( os.path.join(portage.getPackageInstance('win32libs', 'boost-headers').sourceDir(),"tools","build", "bjam.exe" ),
                                   os.path.join( self.imageDir(), "bin", "bjam.exe" ) )


    def make(self):
        if OsUtils.isUnix():
            cmd = "./bootstrap.sh  --with-toolset="
            if compiler.isClang():
                cmd += "clang"
            elif compiler.isGCC():
                cmd += "gcc"
        else:
            cmd = "bootstrap.bat "
            if compiler.isClang():
                cmd += "clang"
            elif compiler.isMinGW():
                cmd += "mingw"
            elif compiler.isMSVC():
                platform = str(compiler.msvcPlatformToolset())
                cmd += f"vc{platform[:2]}"
        utils.system(cmd, cwd = os.path.join(portage.getPackageInstance('win32libs',
                'boost-headers').sourceDir(),"tools","build")) or craftDebug.log.critical(
                "command: %s failed" % (cmd))
        return True


