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
from Packager.PortablePackager import *
from Blueprints.CraftVersion import CraftVersion


class NullsoftInstallerPackager(PortablePackager):
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

    SHORTCUT_SECTION = \
"""
    Section
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    SetOutPath $INSTDIR ; for working directory
    {shortcuts}
    !insertmacro MUI_STARTMENU_WRITE_END
    SectionEnd
"""

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        PortablePackager.__init__(self, whitelists, blacklists)
        self.nsisExe = None
        self._isInstalled = False

    def setDefaults(self, defines) -> {}:
        defines = super().setDefaults(defines)
        defines.setdefault("defaultinstdir", "$PROGRAMFILES64" if CraftCore.compiler.isX64() else "$PROGRAMFILES")
        defines.setdefault("multiuser_use_programfiles64", "!define MULTIUSER_USE_PROGRAMFILES64" if CraftCore.compiler.isX64() else "")
        defines.setdefault("srcdir", self.archiveDir())# deprecated
        defines.setdefault("registy_hook", "")
        defines.setdefault("sections", "")
        defines.setdefault("un_sections", "")
        defines.setdefault("sections_page", "")
        defines.setdefault("preInstallHook", "")


        if not self.scriptname:
            self.scriptname = os.path.join(os.path.dirname(__file__), "Nsis", "NullsoftInstaller.nsi")
        return defines

    def isNsisInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                CraftCore.log.critical("Craft requires Nsis to create a package, please install Nsis\n"
                                       "\t'craft nsis'")
                return False
        return True

    def __isInstalled(self):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        self.nsisExe = CraftCore.cache.findApplication("makensis")
        if not self.nsisExe:
            return False
        return CraftCore.cache.getVersion(self.nsisExe, versionCommand="/VERSION") >= CraftVersion("3.03")

    def _createShortcut(self, name, target, icon="", parameter="", description="") -> str:
        return  f"""CreateShortCut "$SMPROGRAMS\$StartMenuFolder\\{name}.lnk" "$INSTDIR\\{OsUtils.toNativePath(target)}" "{parameter}" "{icon}" 0 SW_SHOWNORMAL "" "{description}"\n"""

    def folderSize(self, path):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += self.folderSize(entry.path)
        return total

    def generateNSISInstaller(self, defines):
        """ runs makensis to generate the installer itself """
        defines["dataPath"] = str(Path(defines["setupname"]).with_suffix( "." + CraftCore.settings.get("Packager", "7ZipArchiveType", "7z")))
        defines["dataName"] = os.path.basename(defines["dataPath"])
        defines["setupname"] = str(Path(defines["setupname"]).with_suffix(".exe"))
        defines["7za"] = CraftCore.cache.findApplication("7za") if CraftCore.compiler.isX64() else CraftCore.cache.findApplication("7za_32")
        # provide the actual installation size in kb, ignore the 7z size as it gets removed after the install
        defines["installSize"] = str(int((self.folderSize(self.archiveDir()) - os.path.getsize(defines["dataPath"])) / 1000))

        defines["installerIcon"] = f"""!define MUI_ICON "{defines["icon"]}" """
        defines["iconname"] = os.path.basename(defines["icon"])
        if not defines["license"] == "":
            defines["license"] = f"""!insertmacro MUI_PAGE_LICENSE "{defines["license"]}" """

        shortcuts = []
        if "executable" in defines:
            shortcuts.append(self._createShortcut(defines["productname"], defines["executable"]))
            del defines["executable"]

        for short in defines["shortcuts"]:
            shortcuts.append(self._createShortcut(**short))
        if shortcuts:
            defines["shortcuts"] = NullsoftInstallerPackager.SHORTCUT_SECTION.format(shortcuts = "".join(shortcuts))


        if defines.get("sections", None):
            defines["sections_page"] = "!insertmacro MUI_PAGE_COMPONENTS"

        uninstallDirs = set()
        uninstallFiles = ["\\uninstall.exe", f"\\{defines['iconname']}"]
        prefixLength = len(self.archiveDir())
        for f in utils.filterDirectoryContent(self.archiveDir()):
            f = Path(f[prefixLength:])
            uninstallFiles.append(f)
            d = f.parent
            while d not in uninstallDirs:
                uninstallDirs.add(d)
                d = d.parent

        defines["uninstallFiles"] = "\n".join([f"Delete \"$INSTDIR{f}\"" for f in uninstallFiles])
        defines["uninstallDirs"] = "\n".join([f"RMDir \"$INSTDIR{x}\"" for x in sorted(uninstallDirs, reverse=True)])

        CraftCore.debug.new_line()
        CraftCore.log.debug(f"generating installer {defines['setupname']}")

        verboseString = "/V4" if CraftCore.debug.verbose() > 0 else "/V3"

        defines.setdefault("nsis_include", f"!addincludedir {os.path.dirname(self.scriptname)}")
        defines["nsis_include_internal"] = f"!addincludedir {os.path.join(os.path.dirname(__file__), 'Nsis')}"
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
            return False
        return utils.sign([defines["setupname"]])

    def createPackage(self):
        """ create a package """
        if not self.isNsisInstalled():
            return False

        CraftCore.log.debug("packaging using the NullsoftInstallerPackager")

        defines = self.setDefaults(self.defines)

        if not super().createPackage():
            return False
        if not self.generateNSISInstaller(defines):
            return False

        destDir, archiveName = os.path.split(defines["setupname"])
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(defines["setupname"])
        return True
