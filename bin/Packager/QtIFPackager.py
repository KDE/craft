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

from Blueprints.MetaInfo import MetaInfo
from Blueprints.CraftDependencyPackage import *
from Packager.SevenZipPackager import *

from Utils import CraftHash
from Blueprints.CraftVersion import *
from Package.VirtualPackageBase import VirtualPackageBase
from CraftOS.osutils import OsUtils

class QtIFPackager(SevenZipPackager):
  # Generate packages that can be used by the qt installer framework
  # to generate a repo or offline installer call "craft --package qt-installer-framework"
  # To manage the packaged dependencies using [Packager]CacheDirectTargetsOnly = True and the use
  # of a package.list is recommended.
  # TODO: the root package is currently hardcoded in __rootPackage

    @InitGuard.init_once
    def __init__(self):
        self.__resources = os.path.join(os.path.dirname(__file__), "QtIF")
        SevenZipPackager.__init__(self)
        self.__packageDir = os.path.join(self.packageDestinationDir(), "qtif")
        self.__sdkMode = OsUtils.isWin() and CraftCore.settings.getboolean("QtSDK", "Enabled", False)
        if self.__sdkMode:
            win = "win32" if CraftCore.compiler.isX86() else "win64"
            self.__imagePrefix = os.path.join(CraftCore.settings.get("QtSDK", "Version"), CraftCore.settings.get("QtSDK", "Compiler"))
            self.__depPrefix = f"{self.__rootPackage}.{CraftCore.settings.get('QtSDK', 'Version').replace('.', '')}.{win}_{CraftCore.settings.get('QtSDK', 'Compiler')}"
        else:
            self.__depPrefix = self.__rootPackage
            self.__imagePrefix = ""

    @property
    def __rootPackage(self):
        #TODO: allow to specify the root node
        return "kdab"

    def __qtiFy(self, package):
        path = f"{self.__depPrefix}.{package.path}"
        return path.replace("/", ".").replace("-", "_")

    def _shortCuts(self, defines):
        out = []
        def shortCut(name, target, icon="", parameter="", description=""):
            target = OsUtils.toUnixPath(os.path.join(self.__imagePrefix, target))
            name = OsUtils.toUnixPath(name)
            if self.__sdkMode:
                name = f"{name} for Qt {CraftCore.settings.get('QtSDK', 'Version')} {CraftCore.settings.get('QtSDK', 'Compiler')}"
            return f'component.addOperation( "CreateShortcut", "@TargetDir@/{target}","@StartMenuDir@/{name}.lnk");'

        if "executable" in defines:
            out += [shortCut(self.subinfo.displayName, defines["executable"])]

        for short in defines["shortcuts"]:
            out += [shortCut(**short)]
        return "\n".join(out)

    def __createMeta(self, defines, *,  dstpath : str, name : str, version : str, description : str, webpage : str, deps : str=""):

        data = {"VERSION" : str(CraftVersion(version).strictVersion),
                "NAME" : name,
                "DESCRIPTION" : cgi.escape(f"{name} {version}<br>{description}" + (f"<br>{webpage}" if webpage else "")),
                "DATE" : datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                "DEPENDENCIES" : deps}
        if not utils.configureFile(os.path.join(self.__resources, "package.xml"), os.path.join(dstpath, "meta", "package.xml"), data):
            return False

        data = {"SHORTCUTS" : self._shortCuts(defines=defines)}
        if not utils.configureFile(os.path.join(self.__resources, "installscript.qs"), os.path.join(dstpath, "meta", "installscript.qs"), data):
            return False
        return True


    def __resolveDeps(self):
        deps = []
        for package in CraftDependencyPackage(self.package).getDependencies(DependencyType.Runtime):
            if isinstance(package.instance, VirtualPackageBase):
                continue
            if package == self.package:
              continue
            # in case we don't want to provide a full installer
            if CraftCore.settings.getboolean("Packager", "CacheDirectTargetsOnly") and package not in CraftCore.state.directTargets:
              continue
            deps += [self.__qtiFy(package)]
        return deps


    def _addPackage(self, defines) -> bool:
        dstpath = os.path.join(self.__packageDir, "image", self.__qtiFy(self.package))
        if not os.path.exists(dstpath):
            if self.__sdkMode:
                # adept the prefix
                utils.cleanDirectory(self.archiveDir())
                utils.copyDir(self.imageDir(), os.path.join(self.archiveDir(), self.__imagePrefix))

            if not self._createArchive("data.7z", self.imageDir() if not self.__sdkMode else self.archiveDir(), os.path.join(dstpath, "data"), createDigests=False, ):
                return False

        info = MetaInfo(self.package)
        return self.__createMeta(defines, dstpath=dstpath , name=info.displayName, version=self.version, description=info.description, webpage=info.webpage, deps=", ".join(self.__resolveDeps()))


    def __initPrefix(self, defines):
        dest = os.path.join(self.__packageDir, "image", self.__depPrefix)
        if not os.path.exists(dest):
            p = CraftPackageObject.get(self.__rootPackage)
            info = MetaInfo(p)

            displayName = info.displayName
            if self.__sdkMode:
                displayName = f"{displayName} for Qt {CraftCore.settings.get('QtSDK', 'Version')} {CraftCore.settings.get('QtSDK', 'Compiler')}"
            return self.__createMeta(defines, dstpath=dest, name=displayName, version="0.0", description=info.description, webpage=info.webpage)
        return True

    def createPackage(self):
        defines = self.setDefaults(self.defines)
        if not self.__initPrefix(defines):
          return False
        return self._addPackage(defines)


