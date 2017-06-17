# -*- coding: utf-8 -*-
import info
from Package import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        self.clang = portage.getPackageInstance('win32libs', 'clang')
        self.lld = portage.getPackageInstance('win32libs', 'lld')
        self.subPackages = [self.clang, self.lld]
        self.subinfo.options.configure.defines = "-DLLVM_TARGETS_TO_BUILD='X86'"
        self.subinfo.options.configure.defines += " -DLLVM_EXTERNAL_LLD_SOURCE_DIR=\"%s\"" % self.lld.sourceDir().replace("\\", "/")
        self.subinfo.options.configure.defines += " -DLLVM_EXTERNAL_CLANG_SOURCE_DIR=\"%s\"" % self.clang.sourceDir().replace("\\", "/")
        if compiler.isMSVC():
            self.subinfo.options.configure.defines += " -DLLVM_EXPORT_SYMBOLS_FOR_PLUGINS=ON"
        else:
            self.subinfo.options.configure.defines += " -DBUILD_SHARED_LIBS=ON"

    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        for p in self.subPackages:
            if not p.fetch():
                return False
        return True

    def unpack(self):
        if not CMakePackageBase.unpack(self):
            return False
        for p in self.subPackages:
            if not p.unpack():
                return False
        return True
    
    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        # just expect that we don't want to debug our compiler
        options += ' -DCMAKE_BUILD_TYPE=Release'
        return options

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if compiler.isMinGW():
            files = os.listdir(os.path.join(self.buildDir(), "lib"))
            for f in files:
                if f.endswith("dll.a"):
                    src = os.path.join(self.buildDir(), "lib", f)
                    dest = os.path.join(self.imageDir(), "lib", f)
                    if not os.path.exists(dest):
                        utils.copyFile(src, dest, False)

        if OsUtils.isWin():
            exeSuffix = ".exe"
        else:
            exeSuffix = ""

        # the build system is broken so....
        src = os.path.join(self.imageDir(), "bin", "clang" + exeSuffix)
        if compiler.isGCC():
            dest = os.path.join(self.imageDir(), "bin", "clang++" + exeSuffix)
        elif compiler.isMSVC():
            dest = os.path.join(self.imageDir(), "bin", "clang-cl" + exeSuffix)
        else:
            craftDebug.log.error("Unknown compiler")
        if not os.path.exists(dest):
            utils.copyFile(src, dest)
        return True
