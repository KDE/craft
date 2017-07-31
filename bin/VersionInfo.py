# -*- coding: utf-8 -*-
# this package contains functions to easily set versions for packages like qt5 or kde
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>
from CraftDebug import craftDebug
from CraftConfig import *
import utils


class VersionInfo(object):
    _VERSION_INFOS = {}
    _VERSION_INFOS_HINTS = {}

    def __init__(self, parent):
        self.subinfo = parent
        self.__defaulVersions = None
        self._fileName = None

    @property
    def _defaulVersions(self):
        if self.__defaulVersions is None:
            name = self.subinfo.parent.filename
            if name in VersionInfo._VERSION_INFOS_HINTS:
                if VersionInfo._VERSION_INFOS_HINTS[name] == None:
                    return None
                else:
                    # utils.debug("Using cached version info for %s in %s" % (name, _VERSION_INFOS_HINTS[ name ]))
                    return VersionInfo._VERSION_INFOS[VersionInfo._VERSION_INFOS_HINTS[name]]
            root = os.path.dirname(name)

            if self._fileName is None:
                possibleInis = [os.path.join(root, "version.ini"), os.path.join(root, "..", "version.ini"),
                                os.path.join(root, "..", "..", "version.ini")]
            else:
                possibleInis = [self._fileName]

            for iniPath in possibleInis:
                iniPath = os.path.abspath(iniPath)
                if iniPath in VersionInfo._VERSION_INFOS.keys():
                    VersionInfo._VERSION_INFOS_HINTS[name] = iniPath
                    craftDebug.log.debug("Found a version info for %s in cache" % name)
                    return VersionInfo._VERSION_INFOS[iniPath]
                elif os.path.exists(iniPath):
                    config = configparser.ConfigParser()
                    config.read(iniPath)
                    VersionInfo._VERSION_INFOS[iniPath] = config
                    VersionInfo._VERSION_INFOS_HINTS[name] = iniPath
                    craftDebug.log.debug("Found a version info for %s in %s" % (name, iniPath))
                    return config
            VersionInfo._VERSION_INFOS_HINTS[name] = None
        return self.__defaulVersions

    def _getVersionInfo(self, key, default=None):
        if self._defaulVersions.has_section("General") and key in self._defaulVersions["General"]:
            return self._defaulVersions["General"][key]
        return default

    def tags(self):
        out = self._getVersionInfo("tags")
        return out.split(";") if out else {}

    def branches(self):
        out = self._getVersionInfo("branches")
        return out.split(";") if out else {}

    def tarballs(self):
        out = self._getVersionInfo("tarballs")
        return out.split(";") if out else {}

    def defaultTarget(self):
        if ("PortageVersions", self.packageName()) in craftSettings:
            return craftSettings.get("PortageVersions", self.packageName())
        name = self._getVersionInfo("name", "")
        if ("PortageVersions", name) in craftSettings:
            return craftSettings.get("PortageVersions", name)
        return self._getVersionInfo("defaulttarget")

    def _replaceVar(self, text, ver, name):
        replaces = {"VERSION": ver, "PACKAGE_NAME": name}

        split_ver = ver.split(".")
        if len(split_ver) == 3:
            replaces["VERSION_MAJOR"] = split_ver[0]
            replaces["VERSION_MINOR"] = split_ver[1]
            replaces["VERSION_PATCH_LEVEL"] = split_ver[2]

        while CraftConfig.variablePatern.search(text):
            for match in CraftConfig.variablePatern.findall(text):
                text = text.replace(match, replaces[match[2:-1].upper()])
        return text

    def setDefaultValuesFromFile(self, fileName, tarballUrl=None, tarballDigestUrl=None, tarballInstallSrc=None,
                                 gitUrl=None):
        self._fileName = os.path.abspath(os.path.join(os.path.dirname(self.subinfo.parent.filename), fileName))
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
        if packageName is None:
            packageName = self.subinfo.package
        if tarballUrl is None:
            tarballUrl = self._getVersionInfo("tarballUrl", None)
        if tarballDigestUrl is None:
            tarballDigestUrl = self._getVersionInfo("tarballDigestUrl", None)
        if tarballInstallSrc is None:
            tarballInstallSrc = self._getVersionInfo("tarballInstallSrc", None)
        if gitUrl is None:
            gitUrl = self._getVersionInfo("gitUrl", None)
        if not tarballUrl is None:
            for ver in self.tarballs():
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.targets[target] = self._replaceVar(tarballUrl, ver, packageName)
                if not tarballDigestUrl is None:
                    self.subinfo.targetDigestUrls[target] = self._replaceVar(tarballDigestUrl, ver, packageName)
                if not tarballInstallSrc is None:
                    self.subinfo.targetInstSrc[target] = self._replaceVar(tarballInstallSrc, ver, packageName)

        if not gitUrl is None:
            for ver in self.branches():
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.svnTargets[ver] = "%s|%s|" % (self._replaceVar(gitUrl, ver, packageName), ver)

            for ver in self.tags():
                target = f"{ver}-{patchLevel}" if patchLevel else ver
                self.subinfo.svnTargets[target] = "%s||%s" % (self._replaceVar(gitUrl, ver, packageName), ver)

        self.subinfo.defaultTarget = f"{self.defaultTarget( ) }-{patchLevel}" if patchLevel else self.defaultTarget()

    def packageName(self):
        return self.subinfo.package
