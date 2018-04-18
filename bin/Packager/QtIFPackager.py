# -*- coding: utf-8 -*-
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

import datetime
import cgi

from Packager.SevenZipPackager import *

from Utils import CraftHash
from Blueprints.CraftVersion import *
from Package.VirtualPackageBase import VirtualPackageBase
from CraftOS.osutils import OsUtils

class QtIFPackager(SevenZipPackager):

    @InitGuard.init_once
    def __init__(self):
        SevenZipPackager.__init__(self)
        self.__resources = os.path.join(os.path.dirname(__file__), "QtIF")
        self.__packageDir = os.path.join(self.packageDestinationDir(), "qtif")
        self.__sdkMode = OsUtils.isWin() and CraftCore.settings.getboolean("QtSDK", "Enabled", False)
        if self.__sdkMode:
            win = "win32" if CraftCore.compiler.isX86() else "win64"
            self.__depPrefix = f"qt.qt5.{CraftCore.settings.get('QtSDK', 'Version').replace('.', '')}.{win}_{CraftCore.settings.get('QtSDK', 'Compiler')}.kde"
            self.__imagePrefix = os.path.join(CraftCore.settings.get("QtSDK", "Version"), CraftCore.settings.get("QtSDK", "Compiler"))
        else:
            self.__imagePrefix = ""

    @property
    def _date(self):
        return datetime.datetime.utcnow().strftime("%Y-%m-%d")

    def qtifyFy(self, package):
            if not self.__sdkMode:
                path = f"kde.{package.path}"
            else:
                path = f"{self.__depPrefix}.{package.name}"
            return path.replace("/", ".").replace("-", "_")

    def _shortCuts(self):
        out = []
        def shortCut(name, target, icon="", parameter="", description=""):
            target = OsUtils.toUnixPath(os.path.join(self.__imagePrefix, target))
            name = OsUtils.toUnixPath(name)
            return f'component.addOperation( "CreateShortcut", "@TargetDir@/{target}","@StartMenuDir@/{name}.lnk");'

        if "executable" in self.defines:
            out += [shortCut(self.subinfo.displayName, self.defines["executable"])]

        for short in self.shortcuts:
            out += [shortCut(**short)]
        return "\n".join(out)

    def _addPackage(self) -> bool:
        if self.__sdkMode:
            # adept the prefix
            utils.cleanDirectory(self.archiveDir())
            utils.copyDir(self.imageDir(), os.path.join(self.archiveDir(), self.__imagePrefix))

        dstpath = os.path.join(self.__packageDir, "image", self.qtifyFy(self.package))
        if not self._compress("data.7z", self.imageDir() if not self.__sdkMode else self.archiveDir(), os.path.join(dstpath, "data"), createDigests=False):
            return False

        deps = []
        for x in self.subinfo.runtimeDependencies.keys():
            # TODO:
            # this filter not installed packages but also packages that are virtual on this platform
            package = CraftPackageObject.get(x)
            if isinstance(package.instance, VirtualPackageBase):
                continue
            if os.path.exists(package.instance.imageDir()):
                deps += [self.qtifyFy(package)]


        data = {"VERSION" : str(CraftVersion(self.version).strictVersion),
                "NAME" : self.subinfo.displayName,
                "DESCRIPTION" : cgi.escape(f"{self.package.name} {self.version}<br>{self.subinfo.description}" + (f"<br>{self.subinfo.webpage}" if self.subinfo.webpage else "")),
                "DATE" : self._date,
                "DEPENDENCIES" : ", ".join(deps)}
        if not utils.configureFile(os.path.join(self.__resources, "package.xml"), os.path.join(dstpath, "meta", "package.xml"), data):
            return False

        data = {"SHORTCUTS" : self._shortCuts()}
        if not utils.configureFile(os.path.join(self.__resources, "installscript.qs"), os.path.join(dstpath, "meta", "installscript.qs"), data):
            return False
        return True


    def __initKDEPrefix(self):

        data = {"VERSION" : "0.0",
                "NAME" : "KDE",
                "DESCRIPTION" : cgi.escape(f"KDE<br>The KDE Community is a free software community dedicated to creating an open and user-friendly computing experience, offering an advanced graphical desktop, a wide variety of applications for communication, work, education and entertainment and a platform to easily build new applications upon. We have a strong focus on finding innovative solutions to old and new problems, creating a vibrant atmosphere open for experimentation.<br>https://www.kde.org/"),
                "DATE" : self._date,
                "DEPENDENCIES" : ""}
        dstpath = os.path.join(self.__packageDir, "image", (self.__depPrefix if self.__sdkMode else "kde"))
        if not utils.configureFile(os.path.join(self.__resources, "package.xml"), os.path.join(dstpath, "meta", "package.xml"), data):
            return False
        return utils.configureFile(os.path.join(self.__resources, "installscript.qs"), os.path.join(dstpath, "meta", "installscript.qs"), {"SHORTCUTS":""})


    def createPackage(self):
        if not self.__initKDEPrefix():
            return False
        return self._addPackage()


