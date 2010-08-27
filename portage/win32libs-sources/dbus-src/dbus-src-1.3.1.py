# -*- coding: utf-8 -*-
import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        svnurl = "https://windbus.svn.sourceforge.net/svnroot/windbus/"
        self.svnTargets['1.2.4'] = svnurl + 'tags/1.2.4'
        self.targetInstSrc['1.2.4'] = 'tags/1.2.4'
        self.targetConfigurePath['1.2.4'] = 'cmake'
        
        self.svnTargets['svnHEAD'] = svnurl + 'trunk'
        self.targetConfigurePath['svnHEAD'] = 'cmake'
        
        # dbus-1.3.1.tar.gz is missing the cmake sub dir and because 
        # emerge is not able yet to apply more than one patch we the 
        # 1.3.1 snapshot took for now
        #self.targets['1.3.1'] = 'http://dbus.freedesktop.org/releases/dbus/dbus-1.3.1.tar.gz'
        #self.targetDigests['1.3.1'] = '83c27e15ba79d4a84a10b123ff382233cc77773b'
        self.targets['1.3.1'] = 'http://cgit.freedesktop.org/dbus/dbus/snapshot/dbus-1.3.1.tar.bz2'
        self.targetDigests['1.3.1'] = 'e8fa74ad6f2294bdf7d22aed25896d8943287c32'
        self.targetInstSrc['1.3.1'] = 'dbus-1.3.1'
        self.targetConfigurePath['1.3.1'] = 'cmake'
        self.patchToApply['gitHEAD'] = [('dbus-scopes.diff', 1)]
        if platform.isCrossCompilingEnabled():
            self.patchToApply['1.3.1'] = [('dbus-1.3.1.diff', 1)]
        else:
            self.patchToApply['1.3.1'] = [('dbus-scopes.diff', 1),('dbus-1.3.1.diff', 1)]
        
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.targetConfigurePath['gitHEAD'] = 'cmake'

        self.defaultTarget = '1.3.1'
        self.options.package.version = '1.3.1-1'
        
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'

from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'dbus'
        self.subinfo.options.make.slnBaseName = 'dbus'
        if (self.buildTarget == '1.3.1' or self.buildTarget == 'gitHEAD') and not platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines = "-DDBUS_ENABLE_XML_DOCS=OFF -DDBUS_USE_EXPAT=ON -DDBUS_SESSION_BUS_DEFAULT_ADDRESS:STRING=autolaunch:scope=install-path"
        else:
            self.subinfo.options.configure.defines = "-DDBUS_ENABLE_XML_DOCS=OFF -DDBUS_USE_EXPAT=ON"
        
    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False      
        if compiler.isMinGW32():
          if self.buildTarget in ['1.2.1', '1.2.3', '1.2.4', 'svnHEAD']:
              utils.copyFile( os.path.join(self.packageDir(), "wspiapi.h"), os.path.join(self.buildDir(), "wspiapi.h") )
        return True

    
if __name__ == '__main__':
    Package().execute()
