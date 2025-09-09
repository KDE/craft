# -*- coding: utf-8 -*-
# Copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# we have to import all packagers because they could be used by the
#   eval(packager)
# call where packager is provided for example on the command line via
#   --option [Packager]PackageType=PortablePackager
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Packager.AppImagePackager import AppImagePackager
from Packager.AppxPackager import AppxPackager  # noqa: F401
from Packager.CMakeApkPackager import CMakeApkPackager
from Packager.CreateArchivePackager import CreateArchivePackager  # noqa: F401
from Packager.InnoSetupPackager import InnoSetupPackager  # noqa: F401
from Packager.MacDMGPackager import MacDMGPackager
from Packager.MacPkgPackager import MacPkgPackager  # noqa: F401
from Packager.NullsoftInstallerPackager import NullsoftInstallerPackager
from Packager.PackagerBase import PackagerBase
from Packager.PortablePackager import PortablePackager  # noqa: F401
from Packager.SevenZipPackager import SevenZipPackager


class TypePackager(PackagerBase):
    """packager that is used in place of different other packagers
    The packager used can be decided at runtime"""

    def __init__(self, package: CraftPackageObject):
        CraftCore.log.debug("TypePackager __init__")
        self.__packager = None
        self.__packageObject = package
        self.changePackager(None)

    def changePackager(self, packager=None):
        if not packager:
            packager = CraftCore.settings.get("Packager", "PackageType", "")

        if not packager:
            if CraftCore.compiler.platform.isWindows:
                packager = NullsoftInstallerPackager
            elif CraftCore.compiler.platform.isMacOS:
                packager = MacDMGPackager
            elif CraftCore.compiler.platform.isLinux:
                packager = AppImagePackager
            elif CraftCore.compiler.platform.isAndroid:
                packager = CMakeApkPackager
            else:
                packager = SevenZipPackager

        if isinstance(packager, str):
            if packager == "MultiCollectionPackager":
                packager = "NullsoftInstallerPackager"
                CraftCore.log.warning("MultiCollectionPackager is deprecated, please use NullsoftInstallerPackager")
            packager = eval(packager)

        if self.__packager:
            bases = list(self.__class__.__bases__)
            for i in range(len(bases)):
                if bases[i] == self.__packager:
                    CraftCore.log.info(f"Replace Packager: {bases[i]} with {packager}")
                    bases[i] = packager
            self.__class__.__bases__ = tuple(bases)
        else:
            self.__class__.__bases__ += (packager,)
        packager.__init__(self, package=self.__packageObject)
        self.__packager = packager

    def createPackage(self):
        return self.__packager.createPackage(self)
