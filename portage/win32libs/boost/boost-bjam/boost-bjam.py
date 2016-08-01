import EmergeDebug
import info
from EmergeOS.osutils import OsUtils

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc = self.package.replace("boost-","").replace("-", "_") )

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
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
            else:
                if compiler.isMSVC2005():
                    cmd += "vc8"
                elif compiler.isMSVC2008():
                    cmd += "vc9"
                elif compiler.isMSVC2010():
                    cmd += "vc10"
                elif compiler.isMSVC2012():
                    cmd += "vc11"
                elif compiler.isMSVC2013():
                    cmd += "vc12"
                elif compiler.isMSVC2015():
                    cmd += "vc14"
        if EmergeDebug.verbose() >= 0:
            print(cmd)
        utils.system(cmd, cwd = os.path.join(portage.getPackageInstance('win32libs',
                'boost-headers').sourceDir(),"tools","build")) or EmergeDebug.die(
                "command: %s failed" % (cmd))
        return True


