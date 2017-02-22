# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    #def setDependencies( self ):

    def setTargets( self ):
        self.svnTargets['master'] = ''
        self.shortDescription = "Review Board Tools."
        self.defaultTarget = 'master'


class Package( PipPackageBase ):
    def __init__( self, **args ):
        PipPackageBase.__init__(self)
        self.python3 = False
        self.allowExternal = True



    def install(self):
        pythonPath = craftSettings.get("Paths","PYTHON27")
        os.makedirs(os.path.join(self.imageDir(), "bin"))
        utils.createBat(os.path.join(self.imageDir(), "bin", "rbt.bat"),
                        "%s %%*" % (os.path.join(pythonPath, "scripts","rbt")))
        return PipBuildSystem.install(self)
