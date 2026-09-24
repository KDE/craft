import os

from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.LinuxDeployPackagerBase import LinuxDeployPackagerBase
from Utils import CraftHash


class AppImagePackager(LinuxDeployPackagerBase):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.AppImage"
        defines.setdefault(
            "runenv",
            [
                # XDG_DATA_DIRS: to make QStandardPaths::GenericDataLocation look in the AppImage paths too.
                # necessary, e.g., to make switching languages for KDE (with KConfigWidgets) applications work.
                # we need to append the default value in any case, since it may not be defined (looking at you, Debian!)
                # in case it is not set by default, UI frameworks won't be able to find files anymore
                # this has caused problems in the past when, e.g., trying to open a browser using QDesktopServices
                'XDG_DATA_DIRS="$this_dir/usr/share/:$XDG_DATA_DIRS:/usr/local/share:/usr/share"',
                'FONTCONFIG_PATH="$(if [ -d /etc/fonts ]; then echo "/etc/fonts"; else echo "$this_dir/etc/fonts"; fi)"',
                'PATH="$this_dir/usr/bin:$this_dir/usr/lib:$PATH"',
            ],
        )
        return defines

    def createPackage(self):
        """create a package"""
        if not self.isLinuxdeployInstalled():
            return False

        CraftCore.log.debug("packaging using the AppImagePackager")

        defines = self.setDefaults(self.defines)
        desktopFile = self._prepareAppDir(defines)
        if not desktopFile:
            return False

        extraEnv = {
            "LDAI_OUTPUT": defines["setupname"],
            "LDNP_META_PACKAGE_NAME": defines.get("appimage_native_package_name", defines["appname"]),
            "LDNP_META_DEB_ARCHITECTURE": CraftCore.compiler.debArchitecture,
            "LDNP_META_RPM_BUILD_ARCH": CraftCore.compiler.rpmArchitecture,
        }

        extraArgs = []
        for output in ["appimage"] + defines.get("appimage_extra_output", []):
            extraArgs += [f"--output={output}"]
        for plugin in ["qt"] + defines.get("appimage_extra_plugins", []):
            extraArgs += [f"--plugin={plugin}"]
        if "appimage_apprun" in defines:
            extraArgs += ["--custom-apprun", defines["appimage_apprun"]]

        if not self._runLinuxDeploy(defines, desktopFile, extraArgs=extraArgs, extraEnv=extraEnv):
            return False

        destDir, archiveName = os.path.split(defines["setupname"])
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(defines["setupname"])
        return True
