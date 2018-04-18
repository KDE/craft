# -*- coding: utf-8 -*-
# Copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# Copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
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

import os

from Utils import CraftHash
from Packager.CollectionPackagerBase import *
from Blueprints.CraftVersion import CraftVersion


class NullsoftInstallerPackager(CollectionPackagerBase):
    """
Packager for Nullsoft scriptable install system

This Packager generates a nsis installer (an executable which contains all files)
from the image directories of craft. This way you can be sure to have a clean
installer.

In your package, you can add regexp whitelists and blacklists (see example files
for the fileformat). The files for both white- and blacklists, must be given already
in the constructor.

You can override the .nsi default script and you will get the following defines
given into the nsis generator via commandline if you do not override the attributes
of the same name in the dictionary self.defines:
setupname:      PACKAGENAME-setup-BUILDTARGET.exe
                PACKAGENAME is the name of the package
srcdir:         is set to the image directory, where all files from the image directories
                of all dependencies are gathered. You shouldn't normally have to set this.
company:        sets the company name used for the registry key of the installer. Default
                value is "KDE".
productname:    contains the capitalized PACKAGENAME and the buildTarget of the current package
executable:     executable is defined empty by default, but it is used to add a link into the
                start menu.
You can add your own defines into self.defines as well.
"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)
        self.nsisExe = None
        self._isInstalled = False

    def _setDefaults(self, defines):
        defines = dict(defines)
        defines.setdefault("architecture", CraftCore.compiler.architecture)
        defines.setdefault("company", "KDE")
        defines.setdefault("defaultinstdir", "$PROGRAMFILES64" if CraftCore.compiler.isX64() else "$PROGRAMFILES")
        defines.setdefault("icon", os.path.join(CraftCore.standardDirs.craftBin(), "data", "icons", "craft.ico"))
        defines.setdefault("license", "")
        defines.setdefault("productname", self.subinfo.displayName)
        defines.setdefault("setupname", self.binaryArchiveName(fileType="exe", includeRevision=True))
        defines.setdefault("srcdir", self.archiveDir())
        defines.setdefault("version", self.sourceRevision() if self.subinfo.hasSvnTarget() else self.version)
        defines.setdefault("website", self.subinfo.webpage if self.subinfo.webpage else "https://community.kde.org/Craft")
        defines.setdefault("registy_hook", "")
        # runtime distributable files
        defines.setdefault("vcredist", self.getVCRedistLocation())

        if not self.scriptname:
            self.scriptname = os.path.join(os.path.dirname(__file__), "NullsoftInstaller.nsi")
        return defines

    def isNsisInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                CraftCore.log.critical("could not find installed nsis package, "
                                        "you can install it using craft nsis or"
                                        "download and install it from "
                                        "http://sourceforge.net/projects/nsis/")
                return False
        return True

    def __isInstalled(self):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        self.nsisExe = CraftCore.cache.findApplication("makensis")
        if not self.nsisExe:
            return False
        return CraftCore.cache.getVersion(self.nsisExe, versionCommand="/VERSION") >= CraftVersion("3.03")

    @staticmethod
    def getVCRuntimeLibrariesLocation():
        """ Note: For MSVC, only: Return base directory for VC runtime distributable libraries """
        if "VCToolsRedistDir" in os.environ:
            return os.environ["VCToolsRedistDir"]
        _path = os.path.join(os.path.dirname(shutil.which("cl.exe")), "..", "redist")
        if not os.path.exists(_path):
            _path = os.path.join(os.path.dirname(shutil.which("cl.exe")), "..", "..", "redist")
        return _path

    @staticmethod
    def getVCRedistLocation():
        if not CraftCore.compiler.isMSVC():
            return "none"
        _file = None
        if CraftCore.compiler.isMSVC():
            arch = "x86"
            if CraftCore.compiler.isX64():
                arch = "x64"

            # TODO: This needs to be made more fail-safe: the version numbers can change with any VS upgrade...
            if CraftCore.compiler.isMSVC2015():
                _file = os.path.join(NullsoftInstallerPackager.getVCRuntimeLibrariesLocation(), "1033", f"vcredist_{arch}.exe")
            elif CraftCore.compiler.isMSVC2017():
                for name in [f"vcredist_{arch}.exe", f"vc_redist.{arch}.exe"]:
                    _file = os.path.join(os.environ["VCTOOLSREDISTDIR"], name)
                    if os.path.isfile(_file):
                        break

            if not os.path.isfile(_file):
                CraftCore.debug.new_line()
                CraftCore.log.critical(
                    "Assuming we can't find a c++ redistributable because the user hasn't got one. Must be fixed manually.")
        return _file

    def _createShortcut(self, name, target, icon="", parameter="", description="") -> str:
        return  f"""CreateShortCut "${{startmenu}}\\{name}.lnk" "$INSTDIR\\{OsUtils.toNativePath(target)}" "{parameter}" "{icon}" 0 SW_SHOWNORMAL "" "{description}"\n"""

    def generateNSISInstaller(self):
        """ runs makensis to generate the installer itself """

        defines = self._setDefaults(self.defines)
        defines["installerIcon"] = f"""!define MUI_ICON "{defines["icon"]}" """
        defines["iconname"] = os.path.basename(defines["icon"])
        if not defines["license"] == "":
            defines["license"] = f"""!insertmacro MUI_PAGE_LICENSE "{defines["license"]}" """

        defines["HKLM"] = "HKLM32" if CraftCore.compiler.isX86() else "HKLM64"
        defines["HKCR"] = "HKCR32" if CraftCore.compiler.isX86() else "HKCR64"
        defines["HKCU"] = "HKCU32" if CraftCore.compiler.isX86() else "HKCU64"


        shortcuts = []
        if "executable" in defines:
            shortcuts.append(self._createShortcut(defines["productname"], defines["executable"]))
            del defines["executable"]

        for short in self.shortcuts:
            shortcuts.append(self._createShortcut(**short))
        defines["shortcuts"] = "".join(shortcuts)

        # make absolute path for output file
        if not os.path.isabs(defines["setupname"]):
            dstpath = self.packageDestinationDir()
            defines["setupname"] = os.path.join(dstpath, defines["setupname"])

        CraftCore.debug.new_line()
        CraftCore.log.debug("generating installer %s" % defines["setupname"])

        verboseString = "/V4" if CraftCore.debug.verbose() > 0 else "/V3"

        cmdDefines = []
        configuredScrip = os.path.join(self.workDir(), f"{self.package.name}.nsi")
        if not utils.configureFile(self.scriptname, configuredScrip, defines):
            configuredScrip = self.scriptname
            # this script uses the old behaviour, using defines
            for key, value in defines.items():
                if value is not None:
                    cmdDefines.append(f"/D{key}={value}")

        if not utils.systemWithoutShell([self.nsisExe, verboseString] + cmdDefines + [configuredScrip],
                                        cwd=os.path.abspath(self.packageDir())):
            CraftCore.log.critical("Error in makensis execution")
            return None
        if not utils.sign([defines["setupname"]]):
            return None
        return defines["setupname"]

    def createPackage(self):
        """ create a package """
        if not self.isNsisInstalled():
            return False

        CraftCore.log.debug("packaging using the NullsoftInstallerPackager")

        if CraftCore.compiler.isMSVC():
            # we use the redist installer
            self.ignoredPackages.append("libs/runtime")
        if not self.internalCreatePackage():
            return False
        setupname = self.generateNSISInstaller()
        if not setupname:
            return False
        destDir, archiveName = os.path.split(setupname)
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(setupname)
        return True
