# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    #def setDependencies( self ):

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.shortDescription = "Doxyqml is an input filter for Doxygen, a documentation system for C++ and a few other languages."
        self.defaultTarget = 'gitHEAD'


class Package( PipPackageBase ):
    def __init__( self, **args ):
        PipPackageBase.__init__(self)
        self.python3 = False



    def install(self):
        pythonPath = emergeSettings.get("Paths","PYTHON27")
        os.makedirs(os.path.join(self.imageDir(), "bin"))
        utils.createBat(os.path.join(self.imageDir(), "bin", "doxyqml.bat"),
                        "%s %s %%*" % (os.path.join(pythonPath, "python") , os.path.join(pythonPath, "scripts", "doxyqml")))
        return PipBuildSystem.install(self)
