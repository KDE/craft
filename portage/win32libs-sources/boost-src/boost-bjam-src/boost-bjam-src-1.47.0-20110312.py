import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):
        version = portage.getPackageInstance('win32libs-bin','boost-headers').subinfo.defaultTarget
        self.targets[version] = ''

        self.defaultTarget = version
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.buildDependencies['win32libs-bin/boost-headers'] = 'default'
        if self.defaultTarget == '1.44.0':
            self.buildDependencies['dev-util/bjam'] = 'default'

from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)

    def install(self):
        if not self.subinfo.defaultTarget == '1.44.0':
            for root, dirs, files in os.walk( os.path.join( portage.getPackageInstance( 'win32libs-bin',
                    'boost-headers' ).sourceDir(), "tools", "build", "v2", "engine" ) ):
                if "bjam.exe" in files:
                    utils.copyFile( os.path.join( root, "bjam.exe" ),
                                   os.path.join( self.imageDir(), "bin", "bjam.exe" ) )
        return True

    def make(self):
        if self.subinfo.defaultTarget == '1.44.0':
            return True
        cmd  = "build.bat "
        if compiler.isMinGW():
            cmd += "gcc"
        else:
            if compiler.isMSVC2005():
                cmd += "vc8"
            elif compiler.isMSVC2008():
                cmd += "vc9"
            elif compiler.isMSVC2010():
                cmd += "vc10"
        if utils.verbose() >= 1:
            print(cmd)
        utils.system(cmd, cwd = os.path.join(portage.getPackageInstance('win32libs-bin',
                'boost-headers').sourceDir(),"tools","build","v2","engine")) or utils.die(
                "command: %s failed" % (cmd))
        return True

if __name__ == '__main__':
    Package().execute()
