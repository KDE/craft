# -*- coding: utf-8 -*-
import base
import os
import utils
import info
import sys

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/utils/krecipes'
        self.targets['2.0-alpha3'] = 'http://sourceforge.net/projects/krecipes/files/krecipes/2.0-alpha3/krecipes-2.0-alpha3.tar.gz'
        self.targetInstSrc['2.0-alpha3'] = 'krecipes-2.0-alpha3'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
