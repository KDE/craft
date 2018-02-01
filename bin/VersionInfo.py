# -*- coding: utf-8 -*-
# this package contains functions to easily set versions for packages like qt5 or kde
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>
import re

from Blueprints.CraftPackageObject import *
from CraftConfig import *
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


    def __init__(self, parent, fileName=None):
        self.subinfo = parent

        self._fileName = fileName
        self._data = None
        self.__include = None

    @property
    def data(self):
        if not self._data:
            package = self.subinfo.package.package
            if not self._fileName:
                filePath = OsUtils.toUnixPath(os.path.dirname(package.source))
                while True:
                    if filePath in CraftPackageObject.rootDirectories():
                        break
                    ini = OsUtils.toUnixPath(os.path.join(filePath, "version.ini"))
                    if os.path.exists(ini):
                        self._fileName = ini
                        break
                    filePath = os.path.dirname(filePath)
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
                            setattr(self._data, k, CraftCore.settings._parseList(self._data.info[k]))

                    CraftCore.log.debug(f"Found a version info for {self.subinfo.package} in {self._fileName}")
        return self._data

    @property
    def _include(self):
        if not self.__include:
            if "include" in self.data.info:
                includePath = self.data.info["include"]
                if not os.path.isabs(includePath):
                    includePath = os.path.join(os.path.dirname(self._fileName), includePath)
                self.__include = VersionInfo(self.subinfo, OsUtils.toUnixPath(includePath))
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
        replaces = {"VERSION": ver, "PACKAGE_NAME": name}

        split_ver = ver.split(".")
        if len(split_ver) == 3:
            replaces["VERSION_MAJOR"] = split_ver[0]
            replaces["VERSION_MINOR"] = split_ver[1]
            replaces["VERSION_PATCH_LEVEL"] = split_ver[2]

        while VersionInfo.variablePatern.search(text):
            for match in VersionInfo.variablePatern.findall(text):
                text = text.replace(match, replaces[match[2:-1].upper()])
        return text

    def setDefaultValuesFromFile(self, fileName, tarballUrl=None, tarballDigestUrl=None, tarballInstallSrc=None,
                                 gitUrl=None):
        self._fileName = os.path.abspath(os.path.join(os.path.dirname(self.subinfo.parent.package.source), fileName))
        self._data = None
        self.setDefaultValues(tarballUrl, tarballDigestUrl, tarballInstallSrc, gitUrl)

    def setDefaultValues(self, tarballUrl=None, tarballDigestUrl=None, tarballInstallSrc=None,
                         gitUrl=None, packageName=None, patchLevel=None):
        """
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
            self._include.setDefaultValues(tarballUrl, tarballDigestUrl, tarballInstallSrc, gitUrl, packageName, patchLevel)

        if packageName is None:
            packageName = self.subinfo.package.package.name
        if tarballUrl is None:
            tarballUrl = self.data.info.get("tarballUrl", None)
        if tarballDigestUrl is None:
            tarballDigestUrl = self.data.info.get("tarballDigestUrl", None)
        if tarballInstallSrc is None:
            tarballInstallSrc = self.data.info.get("tarballInstallSrc", None)
        if gitUrl is None:
            gitUrl = self.data.info.get("gitUrl", None)
        if tarballUrl is not None:
            for ver in self.data.tarballs:
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.targets[target] = self._replaceVar(tarballUrl, ver, packageName)
                if not tarballDigestUrl is None:
                    self.subinfo.targetDigestUrls[target] = self._replaceVar(tarballDigestUrl, ver, packageName)
                if not tarballInstallSrc is None:
                    self.subinfo.targetInstSrc[target] = self._replaceVar(tarballInstallSrc, ver, packageName)

        if not gitUrl is None:
            for ver in self.data.branches:
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.svnTargets[ver] = "%s|%s|" % (self._replaceVar(gitUrl, ver, packageName), ver)

            for ver in self.data.tags:
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.svnTargets[target] = "%s||%s" % (self._replaceVar(gitUrl, ver, packageName), ver)

        defaultTarget = self.defaultTarget()
        if defaultTarget:
            self.subinfo.defaultTarget = f"{defaultTarget}-{patchLevel}" if patchLevel else defaultTarget

    def packageName(self):
        return self.subinfo.package.package.path
