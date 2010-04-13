# -*- coding: utf-8 -*-
import utils
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        svnurl = "https://windbus.svn.sourceforge.net/svnroot/windbus/"
        self.svnTargets['1.2.1'] = svnurl + 'tags/1.2.1'
        self.svnTargets['1.2.3'] = svnurl + 'tags/1.2.3'
        self.svnTargets['1.2.4'] = svnurl + 'tags/1.2.4'
        self.targetInstSrc['1.2.4'] = 'tags/1.2.4'
        self.svnTargets['svnHEAD'] = svnurl + 'trunk'
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.svnTargets['git-wince'] = 'git://repo.or.cz/dbus4win.git|marcus-dbus-master-wince-upstream'
        self.targetInstSrc['git-wince'] = 'dbus4win-wince'

        self.targetConfigurePath['1.2.4'] = 'cmake'
        self.targetConfigurePath['gitHEAD'] = 'cmake'
        self.targetConfigurePath['svnHEAD'] = 'cmake'
        self.targetConfigurePath['git-wince'] = 'cmake'

        if self.hasTargetPlatform():
            self.defaultTarget = 'git-wince'
        else:
            self.defaultTarget = '1.2.4'

    def setDependencies( self ):
        if self.hasTargetPlatform():
            self.hardDependencies['win32libs-sources/libxml2-src'] = 'default'
        else:
            self.hardDependencies['win32libs-bin/libxml2'] = 'default'
            self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'dbus'
        self.subinfo.options.make.slnBaseName = 'dbus'
        if self.hasTargetPlatform():
            self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=OFF"
        else:
            self.subinfo.options.configure.defines = "-DDBUS_USE_EXPAT=ON -DDBUS_DISABLE_EXECUTABLE_DEBUG_POSTFIX=ON"
        
    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        if self.buildTarget in ['1.2.1', '1.2.3', '1.2.4', 'svnHEAD']:
            utils.copyFile( os.path.join(self.packageDir(), "wspiapi.h"), os.path.join(self.buildDir(), "wspiapi.h") )
        return True

    
if __name__ == '__main__':
    Package().execute()
