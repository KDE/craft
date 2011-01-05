# -*- coding: iso-8859-15 -*-
import os
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.60.6'] = 'ftp://ftp.gnu.org/gnu/aspell/aspell-0.60.6.tar.gz'
        self.targetDigests['0.60.6'] = '335bcb560e00f59d89ec9e4c4114c325fb0e65f4'
        self.targetInstSrc['0.60.6'] = 'aspell-0.60.6'
        self.patchToApply['0.60.6'] = ('aspell-0.60.6-20100726.diff', 1)
        self.shortDescription = "A powerful spell checker, designed to replace ispell"
        self.defaultTarget = '0.60.6'
        
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs-bin/win_iconv'] = 'default'

        if emergePlatform.isCrossCompilingEnabled():
            # Take the golden hammer and swing it
            self.dependencies['libs/qt'] = 'default'


from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines = ("-DASPELL_STATIC=ON ")

if __name__ == '__main__':
    Package().execute()
