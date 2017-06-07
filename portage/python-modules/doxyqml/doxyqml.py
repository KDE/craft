# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    #def setDependencies( self ):

    def setTargets( self ):
        self.svnTargets['master'] = ''
        self.shortDescription = "Doxyqml is an input filter for Doxygen, a documentation system for C++ and a few other languages."
        self.defaultTarget = 'master'


class Package( PipPackageBase ):
    def __init__( self, **args ):
        PipPackageBase.__init__(self)
        self.python3 = False
        #the shims are not portable
        self.subinfo.options.package.disableBinaryCache = True



    def install(self):
        pythonPath = craftSettings.get("Paths","PYTHON27")
        utils.createShim(os.path.join(self.imageDir(), "bin", "doxyqml.exe"),
                         os.path.join(pythonPath, "python.exe"),
                         args = os.path.join(pythonPath, "Scripts", "doxyqml"),
                         useAbsolutePath=True)
        return PipBuildSystem.install(self)
