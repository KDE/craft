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

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.0.2"]:
            self.targets[ver] = f"http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/tools_ifw/qt.tools.ifw.30/{ver}ifw-win-x86.7z"
            self.targetInstSrc[ver] = f"Tools/QtInstallerFramework/3.0"
            self.targetDigestUrls[ver] = "http://download.qt.io/online/qtsdkrepository/windows_x86/desktop/tools_ifw/qt.tools.ifw.30/3.0.2ifw-win-x86.7z.sha1"
            self.targetInstallPath[ver] = "dev-utils"


        self.description = "The Qt Installer Framework provides a set of tools and utilities to create installers for the supported desktop Qt platforms: Linux, Microsoft Windows, and Mac OS X."
        self.webpage = "https://wiki.qt.io/Qt-Installer-Framework"

        self.defaultTarget = "3.0.2"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"

    def registerOptions(self):
        self.options.dynamic.registerOption("name", "Craft Installer")
        self.options.dynamic.registerOption("title", "Craft Installer")
        self.options.dynamic.registerOption("version", "0.1")
        self.options.dynamic.registerOption("publisher", "KDE Craft")
        self.options.dynamic.registerOption("targetDir", "@RootDir@\\Craft")
        self.options.dynamic.registerOption("startMenuDir", "Craft")
        self.options.dynamic.registerOption("offlineInstaller", False)
        self.options.dynamic.registerOption("installerName", "CraftInstaller")
        self.options.dynamic.registerOption("repositoryURL", "")
        self.options.dynamic.registerOption("repositoryName", "CraftRepository")


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)


    def createPackage(self):
        # TODO: don't run this in package but in a different ways....
        qtifDir = os.path.join(self.packageDestinationDir(), "qtif", )

        vars = {"NAME" : self.subinfo.options.dynamic.name,
                "VERSION" : self.subinfo.options.dynamic.version,
                "PUBLISHER" : self.subinfo.options.dynamic.publisher,
                "TARGET_DIR" : self.subinfo.options.dynamic.targetDir,
                "START_MENU_DIR" : self.subinfo.options.dynamic.startMenuDir,
                "TITLE" : self.subinfo.options.dynamic.title,

                "REPO_ENABLED" : "0" if self.subinfo.options.dynamic.offlineInstaller else "1",
                "REPO_URL" : self.subinfo.options.dynamic.repositoryURL if self.subinfo.options.dynamic.repositoryURL else f"file:///{OsUtils.toUnixPath(qtifDir)}/repo",
                "REPO_NAME" : self.subinfo.options.dynamic.repositoryName,
                }
        if not utils.configureFile(os.path.join(self.packageDir(), "config.xml"), os.path.join(qtifDir, "config.xml"), vars):
            return False
        if not utils.system(["binarycreator", "-n" if not self.subinfo.options.dynamic.offlineInstaller else "-f",
                             "-c", os.path.join(qtifDir, "config.xml"),
                             "-p", os.path.join(qtifDir, "image"),
                             os.path.join(qtifDir, self.subinfo.options.dynamic.installerName + CraftCore.compiler.executableSuffix)]):
            return False
        if not self.subinfo.options.dynamic.offlineInstaller:
            repoDir = os.path.join(qtifDir, "repo")
            command = ["repogen", "--packages", os.path.join(qtifDir, "image")]
            if os.path.isdir(repoDir):
                command += ["--update"]
            command += [repoDir]
            return utils.system(command)
        return True
