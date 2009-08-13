# -*- coding: utf-8 -*-
import base
import utils
import shutil
from utils import die
import os
import info
import re

from Source.GitSource import *
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.libssh.org/projects/libssh/libssh.git"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class Package(PackageBase, GitSource, CMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        GitSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        PackageBase.__init__(self)
        KDEWinPackager.__init__(self)
        
        self.subinfo.options.configure.defines = "-DWITH_STATIC_LIB=ON"
        
if __name__ == '__main__':
    Package().execute()
