# -*- coding: utf-8 -*-
import info
from Package.PipPackageBase import *


class subinfo(info.infoclass):
    # def setDependencies( self ):

    def setTargets(self):
        self.svnTargets['master'] = ''
        self.description = "Jinja2 is a Python module that implements a simple pythonic template language. "
        self.defaultTarget = 'master'


class Package(PipPackageBase):
    def __init__(self, **args):
        PipPackageBase.__init__(self)
