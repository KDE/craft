# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( packageName = "cfe", gitUrl = "[git]http://llvm.org/git/clang.git")
        self.targetDigests['3.7.0'] = '4ff8100565528b13d99a73f807e9b426c3b3bed9'


        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ver] = [("fix_shortpath.patch", 1)]
            if ver in ["3.7.0", "3.7.1", "release_37"]:
                self.patchToApply[ ver ] += [("0014-use-DESTDIR-on-windows.patch", 1)]
            else:
                self.patchToApply[ver] += [("fix-plugins.diff", 1)]
            if compiler.isMinGW():
                self.patchToApply[ ver ] += [("0012-Set-the-x86-arch-name-to-i686-for-mingw-w64.patch", 1),
                                             ("0015-Fix-the-calling-convention-of-Mingw64-long-double-va.patch", 1),
                                             ("0016-Teach-mingw-toolchain-driver-to-properly-emit-static.patch", 1),
                                             ("0017-Fix-PR23472-by-emitting-initialized-variable-and-its.patch", 1)]


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)


    def configure( self, defines=""):
        return True

    def make( self ):
        return True

    def install( self):
        return True
