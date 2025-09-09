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
import io
import sys
from pathlib import Path

import utils
from CraftCore import CraftCore
from Packager.PackagerBase import PackagerBase


class DesktopEntry(PackagerBase):
    def createPackage(self):
        defines = self.setDefaults(self.defines)
        craftName = CraftCore.standardDirs.craftRoot().name
        if CraftCore.compiler.platform.isMacOS:
            root = CraftCore.standardDirs.craftRoot()
            targetBundle = Path(self.getMacAppPath(defines, root / "Applications"))
            targetPlist = targetBundle / "Contents/Info.plist"
            with io.StringIO() as binaryLog:
                utils.system(
                    ["defaults", "read", targetPlist, "CFBundleExecutable"],
                    stdout=binaryLog,
                )
                targetBinary = binaryLog.getvalue().strip()
            with io.StringIO() as iconLog:
                utils.system(
                    ["defaults", "read", targetPlist, "CFBundleIconFile"],
                    stdout=iconLog,
                )
                targetIcon = iconLog.getvalue().strip()
            if not targetBinary:
                return False
            # install shim to allow invocation of the bunde from the craft env
            if not utils.createShim(
                root / "bin" / defines["display_name"],
                targetBundle / "Contents/MacOS" / targetBinary,
                useAbsolutePath=True,
            ):
                return False
            targetShimBundle = Path("/Applications/Craft", f"{craftName} {defines['display_name']}.app")
            shim = targetShimBundle / "Contents/MacOS" / targetBinary
            if not utils.createDir(targetShimBundle / "Contents/MacOS"):
                return False
            if not utils.createDir(targetShimBundle / "Contents/Resources"):
                return False
            if not utils.createShim(
                shim,
                sys.executable,
                [
                    CraftCore.standardDirs.craftBin() / "craft.py",
                    "--run-detached",
                    targetBundle / "Contents/MacOS" / targetBinary,
                ],
                useAbsolutePath=True,
            ):
                return False
            if not utils.copyFile(targetPlist, targetShimBundle / "Contents/Info.plist", linkOnly=False):
                return False
            if targetIcon and not utils.copyFile(
                targetBundle / "Contents/Resources" / targetIcon,
                targetShimBundle / "Contents/Resources" / targetIcon,
                linkOnly=False,
            ):
                return False
        elif CraftCore.compiler.platform.isWindows:
            shortcuts = defines["shortcuts"] or []
            if "executable" in defines:
                shortcuts.append({"name": defines["productname"], "target": defines["executable"]})
                del defines["executable"]
            for shortcut in shortcuts:
                shim = CraftCore.standardDirs.craftRoot() / "wrapper" / shortcut["name"]
                target = CraftCore.standardDirs.craftRoot() / shortcut["target"]
                if not utils.createShim(
                    shim,
                    sys.executable,
                    [
                        CraftCore.standardDirs.craftBin() / "craft.py",
                        "--run-detached",
                        target,
                    ],
                    guiApp=True,
                ):
                    return False
                if not utils.installShortcut(
                    f"{craftName}/{shortcut['name']} {craftName}",
                    shim,
                    target.parent,
                    CraftCore.standardDirs.craftRoot() / shortcut["target"],
                    shortcut.get(
                        "desciption",
                        f"{shortcut['name']} from {CraftCore.standardDirs.craftRoot()}",
                    ),
                ):
                    return False
        return True
