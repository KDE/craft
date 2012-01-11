# -*- coding: utf-8 -*-
import utils
import os
import info
import emergePlatform
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

        self.targets['1.4.0'] = 'http://cgit.freedesktop.org/dbus/dbus/snapshot/dbus-1.4.0.tar.bz2'
        self.targetDigests['1.4.0'] = '3983d9a1456e5772fa4cb5e2818ed015b2f6131b'
        self.targetInstSrc['1.4.0'] = 'dbus-1.4.0'
        self.targetConfigurePath['1.4.0'] = 'cmake'

        self.targets['1.4.1'] = 'http://dbus.freedesktop.org/releases/dbus/dbus-1.4.1.tar.gz'
        self.targetDigests['1.4.1'] = '112279ff58305027294fe0eb5bee600f68cf0b50'
        self.targetInstSrc['1.4.1'] = 'dbus-1.4.1'
        self.targetConfigurePath['1.4.1'] = 'cmake'

        for ver in ['1.4.6', '1.4.8', '1.4.10', '1.4.12', '1.4.14','1.4.16']:
            self.svnTargets[ver] = 'git://anongit.freedesktop.org/git/dbus/dbus||dbus-' + ver
            self.targetSrcSuffix[ver] = 'git'
            self.targetConfigurePath[ver] = 'cmake'

        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.targetConfigurePath['gitHEAD'] = 'cmake'


        if emergePlatform.isCrossCompilingEnabled():
            self.patchToApply['1.4.0'] = [('dbus-1.4.0.diff', 1),
                                          ('0001-tentative-workaround-for-the-random-hangs-on-windows.patch', 1),
                                          ('no-auth.diff', 1),
                                          ('msvc2010-has-errnoh.diff', 1),
                                          ('live-lock-fix.diff', 1),
                                          ('wince-splashscreen.diff', 1)
                                          ]
            self.patchToApply['1.4.1'] = [('no-auth.diff', 1),
                                          ('msvc2010-has-errnoh.diff', 1),
                                          ]
        else:
            self.patchToApply['1.4.0'] = [('dbus-1.4.0.diff', 1),
                                          ('0001-tentative-workaround-for-the-random-hangs-on-windows.patch', 1),
                                          ('msvc2010-has-errnoh.diff', 1),
                                          ('live-lock-fix.diff', 1)
                                          ]
            self.patchToApply['1.4.1'] = [('msvc2010-has-errnoh.diff', 1),
                                          ('live-lock-fix.diff', 1),
                                          ('replace_path_with_current_installdir.diff', 1)
                                         ]
            self.patchToApply['1.4.6'] = [('live-lock-fix.diff', 1),
                                          ('0001-Do-not-use-ELEMENT_TYPE-which-is-reserved.patch', 1)
                                         ]
            self.patchToApply['1.4.10'] = [('workaround-for-inline-keyword-in-msvc10.patch', 1)
                                         ]

        self.shortDescription = "Freedesktop message bus system (daemon and clients)"
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = '1.4.0'
        else:
            self.defaultTarget = '1.4.16'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'dbus'
        self.subinfo.options.make.slnBaseName = 'dbus'
        self.subinfo.options.configure.defines = (
                "-DDBUS_BUILD_TESTS=OFF "
                "-DDBUS_ENABLE_XML_DOCS=OFF "
                "-DDBUS_USE_EXPAT=ON "
                "-DDBUS_REPLACE_LOCAL_DIR=ON ")

        if (self.buildType == "Release"):
            self.subinfo.options.configure.defines += (
                    "-DDBUS_ENABLE_VERBOSE_MODE=OFF "
                    "-DDBUS_DISABLE_ASSERTS=ON ")

        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += (
                    "-DDBUS_SESSION_BUS_DEFAULT_ADDRESS:"
                    "STRING=tcp:host=localhost,port=12434 ")
        else:
            # for 1.4.1 and greater switch to official
            # supported scopes -> autolaunch:scope=*install-path
            self.subinfo.options.configure.defines += (
                    "-DDBUS_SESSION_BUS_DEFAULT_ADDRESS:"
                    "STRING=autolaunch:scope=install-path ")
            # kde uses debugger output, so dbus should do too
            # not sure if this works for wince too, so limited to win32
            self.subinfo.options.configure.defines += (
                    "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON ")

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        if compiler.isMinGW32():
          if self.buildTarget in ['1.2.1', '1.2.3', '1.2.4', 'svnHEAD']:
              utils.copyFile( os.path.join(self.packageDir(), "wspiapi.h"),
                      os.path.join(self.buildDir(), "wspiapi.h") )
        return True


if __name__ == '__main__':
    Package().execute()
