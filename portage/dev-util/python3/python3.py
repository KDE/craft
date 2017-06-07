import os

import info
import compiler
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["3"] = ""
        self.defaultTarget = "3"
        self.targetInstallPath["3"] = "dev-utils"



class Package( BinaryPackageBase ):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.package.disableBinaryCache = True

    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        if not ("Paths","PYTHON") in craftSettings or \
                not os.path.isfile(os.path.join(craftSettings.get("Paths","PYTHON"), "python.exe")):
            craftDebug.log.critical("Please make sure that\n"
                                    "\t[Paths]\n"
                                    "\tPython\n"
                                    "Points to a valid Python installation.")
            return False
        return utils.createShim(os.path.join(self.installDir(), "bin", "python3.exe"),
                                os.path.join(craftSettings.get("Paths","PYTHON"), "python.exe"),
                                useAbsolutePath=True)
