# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    #def setDependencies( self ):

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'


class Package( PipPackageBase ):
    def __init__( self, **args ):
        PipPackageBase.__init__(self)
        self.python2 = False
        

    def install(self):
        pythonPath = craftSettings.get("Paths","PYTHON")
        os.makedirs(os.path.join(self.imageDir(), "bin"))
        utils.createBat(os.path.join(self.imageDir(), "bin", "pylint.bat"),
                        "%s %%*" % (os.path.join(pythonPath, "scripts","pylint")))
        return PipBuildSystem.install(self)
