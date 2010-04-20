# -*- coding: utf-8 -*-
import utils
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        svnurl = "https://windbus.svn.sourceforge.net/svnroot/windbus/"
        self.svnTargets['1.2.4'] = svnurl + 'tags/1.2.4'
        self.targetInstSrc['1.2.4'] = 'tags/1.2.4'
        self.svnTargets['svnHEAD'] = svnurl + 'trunk'
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'

        self.targetConfigurePath['1.2.4'] = 'cmake'
        self.targetConfigurePath['gitHEAD'] = 'cmake'
        self.targetConfigurePath['svnHEAD'] = 'cmake'

        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        if utils.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/libxml2-src'] = 'default'

from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'dbus'
        self.subinfo.options.make.slnBaseName = 'dbus'
        if self.isTargetBuild():
            self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=OFF"
        else:
            self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=ON"
        
    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        if self.buildTarget in ['1.2.1', '1.2.3', '1.2.4', 'svnHEAD']:
            utils.copyFile( os.path.join(self.packageDir(), "wspiapi.h"), os.path.join(self.buildDir(), "wspiapi.h") )
        return True

    
if __name__ == '__main__':
    Package().execute()
