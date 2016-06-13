# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.8.4', '1.10.4']:
            self.targets[ver] = 'http://dbus.freedesktop.org/releases/dbus/dbus-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'dbus-%s' % ver
            self.targetConfigurePath[ver] = 'cmake'

        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/dbus/dbus'
        self.targetSrcSuffix['gitHEAD'] = 'git'
        self.targetConfigurePath['gitHEAD'] = 'cmake'

        self.patchToApply['1.8.4'] = [('dont_include_afxres.diff', 1)]
        self.patchToApply['1.10.4'] = [('dont_include_afxres.diff', 1)]
        self.targetDigests['1.10.4'] = 'ec1921a09199c81ea20b20448237146a414d51ae'

        self.shortDescription = "Freedesktop message bus system (daemon and clients)"
        self.homepage = "http://www.freedesktop.org/wiki/Software/dbus/"
        self.defaultTarget = '1.10.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/expat'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.package.packageName = 'dbus'
        self.subinfo.options.make.slnBaseName = 'dbus'
        self.subinfo.options.configure.defines = (
                "-DDBUS_BUILD_TESTS=OFF "
                "-DDBUS_ENABLE_XML_DOCS=OFF ")

        if (self.buildType() == "Release"):
            self.subinfo.options.configure.defines += (
                    "-DDBUS_ENABLE_VERBOSE_MODE=OFF "
                    "-DDBUS_DISABLE_ASSERTS=ON ")

        self.subinfo.options.configure.defines += (
            "-DDBUS_SESSION_BUS_LISTEN_ADDRESS:STRING=autolaunch:scope=*install-path "
            "-DDBUS_SESSION_BUS_CONNECT_ADDRESS:STRING=autolaunch:scope=*install-path ")
        # kde uses debugger output, so dbus should do too
        self.subinfo.options.configure.defines += (
                "-DDBUS_USE_OUTPUT_DEBUG_STRING=ON ")

    def install( self ):
        if not CMakePackageBase.install( self ): return False

        # TODO: fix
        if self.buildType() == "Debug":
            imagedir = os.path.join( self.installDir(), "lib" )
            if compiler.isMSVC():
                if os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1d.lib"), os.path.join(imagedir, "dbus-1.lib"))
                if not os.path.exists(os.path.join(imagedir, "dbus-1d.lib")):
                    utils.copyFile(os.path.join(imagedir, "dbus-1.lib"), os.path.join(imagedir, "dbus-1d.lib"))
            if compiler.isMinGW():
                if os.path.exists(os.path.join(imagedir, "libdbus-1.dll.a")):
                        utils.copyFile( os.path.join(imagedir, "libdbus-1.dll.a"), os.path.join(imagedir, "libdbus-1d.dll.a") )

        return True


