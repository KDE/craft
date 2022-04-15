# -*- coding: utf-8 -*-
# Copyright (c) 2010 Patrick Spendrin <ps_ml@gmx.de>
# Copyright (c) 2010 Andre Heinecke <aheinecke@intevation.de> (code taken from the kdepim-ce-package.py)
# Copyright Hannah von Reth <vonreth@kde.org>
# Copyright (c) 2022 Thomas Friedrichsmeier <thomas.friedrichsmeier@kdemail.net>
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

from Utils import CraftHash, CodeSign
from Packager.CollectionPackagerBase import *
from Packager.PortablePackager import *
from Blueprints.CraftVersion import CraftVersion


class InnoSetupPackager(PortablePackager):
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
        PortablePackager.__init__(self, whitelists, blacklists)
        self.nsisExe = None
        self._isInstalled = False

    def setDefaults(self, defines) -> {}:
        defines = super().setDefaults(defines)
        defines.setdefault("srcdir", self.archiveDir())# deprecated

        if not self.scriptname:
            self.scriptname = os.path.join(os.path.dirname(__file__), "InnoSetupTemplate.iss")
        return defines

    def isInnoInstalled(self):
        if not self._isInstalled:
            self._isInstalled = self.__isInstalled()
            if not self._isInstalled:
                CraftCore.log.critical("Craft requires InnoSetup to create a package, please install InnoSetup\n"
                                       "\t'craft innosetup'")
                return False
        return True

    def __isInstalled(self):
        """ check if nsis (Nullsoft scriptable install system) is installed somewhere """
        self.innoExe = CraftCore.cache.findApplication("ISCC")
        if not self.innoExe:
            return False
        return True

    def _createShortcut(self, name, target, icon="", parameter="", description="", workingDirectory=None) -> str:
        return f"""Name: "{{group}}\\{name}" ; Filename: "{{app}}\\{OsUtils.toNativePath(target)}" ; WorkingDir: "{workingDirectory}" ; Parameters: "{parameter}" ; IconFileName: "{icon}" ; Comment : "{description}"\n"""

    def generateInnoInstaller(self, defines):
        """ runs ISCC to generate the installer itself """
        defines["setupname"] = str(Path(defines["setupname"]).with_suffix(".exe"))
        if not defines["license"] == "":
            defines["license"] = f"""LicenseFile="{defines["license"]}" """
        if not defines["readme"] == "":
            defines["readme"] = f"""InfoBeforeFile="{defines["readme"]}" """

        shortcuts = []
        if "executable" in defines:
            shortcuts.append(self._createShortcut(defines["productname"], defines["executable"]))
            del defines["executable"]

        for short in defines["shortcuts"]:
            shortcuts.append(self._createShortcut(**short))
        if shortcuts:
            defines["shortcuts"] = "".join(shortcuts)

        CraftCore.debug.new_line()
        CraftCore.log.debug(f"generating installer {defines['setupname']}")

        verboseString = "/V4" if CraftCore.debug.verbose() > 0 else "/V1"

        cmdDefines = []
        cmdDefines.append(f"""/O{os.path.dirname(defines["setupname"])}""")
        cmdDefines.append(f"""/F{str(Path(os.path.basename(defines["setupname"])).with_suffix(""))}""")
        configuredScrip = os.path.join(self.workDir(), f"{self.package.name}.iss")
        utils.configureFile(self.scriptname, configuredScrip, defines)

        if not utils.systemWithoutShell([self.innoExe, verboseString] + cmdDefines + [configuredScrip],
                                        cwd=os.path.abspath(self.packageDir())):
            CraftCore.log.critical("Error in ISCC execution")
            return False
        return CodeSign.signWindows([defines["setupname"]])

    def createPackage(self):
        """ create a package """
        if not self.isInnoInstalled():
            return False

        CraftCore.log.debug("packaging using the InnoSetupPackager")

        defines = self.setDefaults(self.defines)

        if not self.internalCreatePackage(defines, True):
            return False
        if not self.generateInnoInstaller(defines):
            return False

        destDir, archiveName = os.path.split(defines["setupname"])
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(defines["setupname"])
        return True
