# -*- coding: utf-8 -*-
import info
import os
import shutil

from Package.QMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'

        
    def setTargets( self ):
        self.targets['0.7.0'] = 'http://switch.dl.sourceforge.net/project/hupnp/hupnp/herqq-0.7.0.zip'
        self.patchToApply['0.7.0'] = ('herqq-0.7.0-20101111.diff',1)
        self.targetDigests['0.7.0'] = 'e5f7338313030b6915d0cdc3116ddd87a439def9'
        self.targetInstSrc['0.7.0'] = 'herqq-0.7.0'
        self.defaultTarget = '0.7.0'
         

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__(self)
        if self.buildType() == "Debug":
            self.subinfo.options.make.makeOptions = "debug"
        else:
            self.subinfo.options.make.makeOptions = "release"
        os.unsetenv("MAKE")
        os.unsetenv("EMERGE_MAKE_PROGRAM")
        
    def install(self):
        if not QMakeBuildSystem.install(self):
            return False
        shutil.copytree(os.path.join(self.buildDir(),"hupnp","bin"),os.path.join(self.imageDir(),"bin"),ignore=shutil.ignore_patterns('*.a','*.exe'))
        shutil.copytree(os.path.join(self.buildDir(),"hupnp","bin"),os.path.join(self.imageDir(),"lib"),ignore=shutil.ignore_patterns('*.dll','*.exe'))
        shutil.copytree(os.path.join(self.sourceDir(),"hupnp","deploy","include"),os.path.join(self.imageDir(),"include"))
        shutil.copy(os.path.join(self.sourceDir(),"hupnp","lib","qtsoap-2.7-opensource","src","qtsoap.h"),os.path.join(self.imageDir(),"include","qtsoap.h"))
        return True
        
        
        

if __name__ == '__main__':
    Package().execute()
