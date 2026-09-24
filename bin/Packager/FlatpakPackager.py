import os
from pathlib import Path

import utils
from CraftBase import InitGuard
from CraftCore import CraftCore
from Packager.LinuxDeployPackagerBase import LinuxDeployPackagerBase
from Utils import CraftHash


class FlatpakPackager(LinuxDeployPackagerBase):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flatpakExe = None

    def setDefaults(self, defines: set[str, str]) -> set[str, str]:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.flatpak"
        defines.setdefault(
            "runenv",
            [
                "FONTCONFIG_PATH=/etc/fonts",
            ],
        )
        return defines

    def isFlatpakInstalled(self):
        if not self.flatpakExe:
            self.flatpakExe = CraftCore.cache.findApplication("flatpak")
            if not self.flatpakExe:
                CraftCore.log.critical("Craft requires flatpak to create a Flatpak package, please install flatpak\n")
                return False
        return True

    def createPackage(self):
        """create a package"""
        if not self.isLinuxdeployInstalled() or not self.isFlatpakInstalled():
            return False

        CraftCore.log.debug("packaging using the FlatpakPackager")

        defines = self.setDefaults(self.defines)
        desktopFile = self._prepareAppDir(defines)
        if not desktopFile:
            return False

        extraArgs = []
        for plugin in ["qt"] + defines.get("flatpak_extra_plugins", defines.get("appimage_extra_plugins", [])):
            extraArgs += [f"--plugin={plugin}"]

        if not self._runLinuxDeploy(defines, desktopFile, extraArgs=extraArgs):
            return False

        appId = defines.get("flatpak_id", defines.get("app_id", None))
        if not appId:
            stem = Path(desktopFile).stem
            if stem.count(".") >= 2:
                appId = stem
            else:
                baseName = stem if stem else defines["appname"]
                appId = f"org.kde.{baseName}"
                if appId.count(".") < 2:
                    appId = f"org.kde.{appId}"

        appDesktopFile = self.archiveDir() / f"usr/share/applications/{appId}.desktop"
        if not appDesktopFile.exists() and os.path.exists(desktopFile):
            utils.moveFile(desktopFile, appDesktopFile)

        if not utils.moveDir(self.archiveDir() / "usr", self.archiveDir() / "files"):
            return False

        command = defines.get("flatpak_command", defines.get("command", defines["desktopFile"]))
        branch = defines.get("flatpak_branch", "master")
        arch = CraftCore.compiler.appImageArchitecture
        runtime = defines.get("flatpak_runtime", "org.freedesktop.Platform")
        runtimeVersion = defines.get("flatpak_runtime_version", "25.08")

        runtimeRef = runtime if "/" in runtime else f"{runtime}/{arch}/{runtimeVersion}"

        if "flatpak_metadata" in defines:
            metadata = defines["flatpak_metadata"]
        else:
            shared = ";".join(defines.get("flatpak_shared_permissions", ["network", "ipc"])) + ";"
            sockets = ";".join(defines.get("flatpak_socket_permissions", ["x11", "wayland", "fallback-x11", "pulseaudio"])) + ";"
            devices = ";".join(defines.get("flatpak_device_permissions", ["dri"])) + ";"
            filesystems = ";".join(defines.get("flatpak_filesystem_permissions", ["host", "xdg-config/kdeglobals:ro"])) + ";"
            env = "\n".join(defines["runenv"])
            metadata = (
                "[Application]\n"
                f"name={appId}\n"
                f"runtime={runtimeRef}\n"
                f"command={command}\n\n"
                f"[Context]\n"
                f"shared={shared}\n"
                f"sockets={sockets}\n"
                f"devices={devices}\n"
                f"filesystems={filesystems}\n"
                "[Environment]\n"
                f"{env}"
            )

        with (self.archiveDir() / "metadata").open("wt", encoding="UTF-8") as f:
            f.write(metadata)

        finishArgs = [self.flatpakExe, "build-finish", f"--command={command}", str(self.archiveDir())]
        if not utils.system(finishArgs):
            return False

        repoDir = self.archiveDir() / "flatpak-repo"
        if repoDir.exists():
            utils.rmtree(repoDir)
        utils.createDir(repoDir)

        exportArgs = [self.flatpakExe, "build-export", str(repoDir), str(self.archiveDir()), branch]
        if not utils.system(exportArgs):
            return False

        setupname = Path(defines["setupname"])
        if setupname.exists():
            utils.deleteFile(setupname)

        bundleArgs = [self.flatpakExe, "build-bundle", str(repoDir), str(setupname), appId, branch]
        if not utils.system(bundleArgs):
            return False

        destDir, archiveName = os.path.split(setupname)
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(setupname)
        return True
