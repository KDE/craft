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

import configparser
import os
import re
from pathlib import Path

from Blueprints.CraftPackageObject import BlueprintException, CraftPackageObject
from CraftCore import CraftCore


class VersionInfo(object):
    variablePatern = re.compile(r"\$\{[A-Za-z0-9_]*\}", re.IGNORECASE)
    _VERSION_INFOS = {}

    class VersionInfoData(object):
        def __init__(self):
            self.tags = []
            self.branches = []
            self.tarballs = []
            self.info = {}

    def __init__(self, subinfo=None, fileName=None, package=None):
        self.subinfo = subinfo
        if package:
            self.package = package
        elif subinfo:
            self.package = subinfo.parent.package
        else:
            raise Exception()

        self._fileName = Path(fileName) if fileName else None
        self._data = None
        self.__include = None

    @property
    def data(self):
        if not self._data:
            if not self._fileName:
                filePath = self.package.filePath
                while True:
                    if filePath in CraftPackageObject.rootDirectories():
                        raise BlueprintException(
                            "setDefaultValues() called without providing a version.ini",
                            self.package,
                        )
                    ini = filePath / "version.ini"
                    if ini.exists():
                        self._fileName = ini
                        break
                    filePath = filePath.parent
            if not self._fileName:
                self._data = VersionInfo.VersionInfoData()
            else:
                if self._fileName in VersionInfo._VERSION_INFOS:
                    self._data = VersionInfo._VERSION_INFOS[self._fileName]
                else:
                    self._data = VersionInfo.VersionInfoData()
                    VersionInfo._VERSION_INFOS[self._fileName] = self._data
                    config = configparser.ConfigParser()
                    config.read(self._fileName)
                    self._data.info = config["General"]
                    for k in ["tags", "branches", "tarballs"]:
                        if k in self._data.info:
                            setattr(
                                self._data,
                                k,
                                CraftCore.settings._parseList(self._data.info[k]),
                            )

                    CraftCore.log.debug(f"Found a version info for {self.package} in {self._fileName}")
        return self._data

    @property
    def _include(self):
        if not self.__include:
            if "include" in self.data.info:
                includePath = Path(self.data.info["include"])
                if not includePath.is_absolute():
                    includePath = self._fileName.parent / includePath
                self.__include = VersionInfo(subinfo=self.subinfo, package=self.package, fileName=includePath)
        return self.__include

    def tags(self):
        if self._include:
            return self.data.tags + self._include.tags()
        return self.data.tags

    def branches(self):
        if self._include:
            return self.data.branches + self._include.branches()
        return self.data.branches

    def tarballs(self):
        if self._include:
            return self.data.tarballs + self._include.tarballs()
        return self.data.tarballs

    def defaultTarget(self):
        return self.data.info.get("defaulttarget", None)

    @staticmethod
    def _replaceVar(text, ver, name):
        replaces = {
            "VERSION": ver,
            "PACKAGE_NAME": name,
            "COMPILER_BITS": CraftCore.compiler.architecture.bits,
            "COMPILER_ARCHITECTURE": CraftCore.compiler.architecture.key.name,
        }

        split_ver = ver.split(".")
        if len(split_ver) == 3:
            replaces["VERSION_MAJOR"] = split_ver[0]
            replaces["VERSION_MINOR"] = split_ver[1]
            replaces["VERSION_PATCH_LEVEL"] = split_ver[2]

        while VersionInfo.variablePatern.search(text):
            for match in VersionInfo.variablePatern.findall(text):
                text = text.replace(match, replaces[match[2:-1].upper()])
        return text

    def format(self, s: str, ver: str):
        return VersionInfo._replaceVar(s, ver, self.package.name)

    def get(self, key: str, fallback=configparser._UNSET):
        platformKey = f"{key}_{CraftCore.compiler.platform.name}"
        if platformKey in self.data.info:
            return self.data.info.get(platformKey)
        return self.data.info.get(key, fallback)

    def setDefaultValuesFromFile(
        self,
        fileName,
        tarballUrl=None,
        tarballDigestUrl=None,
        tarballInstallSrc=None,
        gitUrl=None,
    ):
        self._fileName = os.path.abspath(os.path.join(os.path.dirname(self.package.source), fileName))
        self._data = None
        self.setDefaultValues(tarballUrl, tarballDigestUrl, tarballInstallSrc, gitUrl)

    def setDefaultValues(
        self,
        tarballUrl=None,
        tarballDigestUrl=None,
        tarballInstallSrc=None,
        gitUrl=None,
        packageName=None,
        patchLevel=None,
    ):
        r"""
        Set svn and tarball targets based on the settings in the next version.ini
        Parameters may contain ${} Variables which then will be replaces.
        Available variables:
        ${PACKAGE_NAME} : The name of the package
        ${VERSION} : The version of the package defined in version.ini
        If the version matches \d.\d.\d there is also avalible:
            ${VERSION_MAJOR} : The first part of ${VERSION}
            ${VERSION_MINOR} : The secon part of ${VERSION}
            ${VERSION_PATCH_LEVEL} : The the third part of ${VERSION}

        """
        if self._include:
            self._include.setDefaultValues(
                tarballUrl,
                tarballDigestUrl,
                tarballInstallSrc,
                gitUrl,
                packageName,
                patchLevel,
            )

        if packageName is None:
            packageName = self.subinfo.parent.package.name
        if tarballUrl is None:
            tarballUrl = self.get("tarballUrl", None)
        if tarballDigestUrl is None:
            tarballDigestUrl = self.get("tarballDigestUrl", None)
        if tarballInstallSrc is None:
            tarballInstallSrc = self.get("tarballInstallSrc", None)
        if gitUrl is None:
            gitUrl = self.get("gitUrl", None)
        gitDirSuffix = self.get("gitDirSuffix", None)
        gitUpdatedRepoUrls = CraftCore.settings._parseList(self.get("gitUpdatedRepoUrl", ""))
        if tarballUrl is not None:
            for target in self.data.tarballs:
                self.subinfo.targets[target] = self._replaceVar(tarballUrl, target, packageName)
                if patchLevel:
                    self.subinfo.patchLevel[target] = patchLevel
                if tarballDigestUrl is not None:
                    self.subinfo.targetDigestUrls[target] = self._replaceVar(tarballDigestUrl, target, packageName)
                if tarballInstallSrc is not None:
                    self.subinfo.targetInstSrc[target] = self._replaceVar(tarballInstallSrc, target, packageName)

        if gitUrl:
            for target in self.data.branches:
                self.subinfo.svnTargets[target] = f"{self._replaceVar(gitUrl, target, packageName)}|{target}|"
                if patchLevel:
                    self.subinfo.patchLevel[target] = patchLevel
                if gitDirSuffix:
                    self.subinfo.targetSrcSuffix[target] = gitDirSuffix

            for target in self.data.tags:
                self.subinfo.svnTargets[target] = f"{self._replaceVar(gitUrl, target, packageName)}||{target}"
                if patchLevel:
                    self.subinfo.patchLevel[target] = patchLevel

            if len(gitUpdatedRepoUrls) == 2:
                for target in self.data.tags + self.data.branches:
                    self.subinfo.targetUpdatedRepoUrl[target] = (
                        self._replaceVar(gitUpdatedRepoUrls[0], target, packageName),
                        self._replaceVar(gitUpdatedRepoUrls[1], target, packageName),
                    )
            elif len(gitUpdatedRepoUrls) > 2:
                raise Exception("gitUpdatedRepoUrls must be a list of the lenght 2")

        defaultTarget = self.defaultTarget()
        if defaultTarget:
            self.subinfo.defaultTarget = defaultTarget
