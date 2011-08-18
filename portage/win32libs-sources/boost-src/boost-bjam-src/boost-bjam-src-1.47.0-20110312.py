import os
import shutil

import utils
import base
import info
import compiler

class subinfo(info.infoclass):
    def setTargets(self):    
        version = portage.getPackageInstance('win32libs-bin', 'boost-headers').subinfo.defaultTarget
        self.targets[version] = ''
        
        self.defaultTarget = version
        self.shortDescription = "portable C++ libraries"

    def setDependencies(self):
        self.dependencies['win32libs-bin/boost-headers'] = 'default'
        if self.defaultTarget == '1.44.0':
            self.buildDependencies['dev-util/bjam'] = 'default'
        
from Package.BoostPackageBase import *

class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        BoostPackageBase.__init__(self)
        
       
       
    def install(self):
        if not self.subinfo.defaultTarget == '1.44.0':
            path, bjam = self._walk(os.path.join(portage.getPackageInstance('win32libs-bin', 'boost-headers').sourceDir(),"tools","build","v2","engine"),"bjam.exe")
            utils.copyFile(os.path.join(path,"bjam.exe"), os.path.join(self.imageDir(), "bin" , "bjam.exe"))
        return True
        
    def make(self):
        if self.subinfo.defaultTarget == '1.44.0':
            return True
        cmd  = "cd %s && build.bat " % os.path.join(portage.getPackageInstance('win32libs-bin', 'boost-headers').sourceDir(),"tools","build","v2","engine")
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
            print cmd
        os.system(cmd) and utils.die(
                "command: %s failed" % (cmd))
        return True

if __name__ == '__main__':
    Package().execute()
