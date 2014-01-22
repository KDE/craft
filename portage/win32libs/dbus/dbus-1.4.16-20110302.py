# -*- coding: utf-8 -*-
import utils
import os
import info
import emergePlatform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.6.8','1.6.14']:
            self.targets[ver] = 'http://dbus.freedesktop.org/releases/dbus/dbus-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'dbus-%s' % ver
            self.targetConfigurePath[ver] = 'cmake'

        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.targetConfigurePath['gitHEAD'] = 'cmake'

        self.shortDescription = "Freedesktop message bus system (daemon and clients)"
        self.defaultTarget = '1.6.14'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/expat'] = 'default'

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
        elif self.buildTarget == "gitHEAD":
            self.subinfo.options.configure.defines += (
                "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path "
                "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path ")
            # kde uses debugger output, so dbus should do too
            self.subinfo.options.configure.defines += (
                    "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON ")
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

if __name__ == '__main__':
    Package().execute()
