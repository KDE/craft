from Packager.CollectionPackagerBase import *

class AppImagePackager(CollectionPackagerBase):
    @InitGuard.init_once
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        defines["setupname"] = f"{defines['setupname']}.AppImage"
        return defines

    def createPackage( self ):
        """ create a package """
        CraftCore.log.debug("packaging using the AppImagePackager")

        archiveDir = Path(self.archiveDir())
        defines = self.setDefaults(self.defines)
        if not self.internalCreatePackage(defines, packageSymbols=False):
            return False
        if not utils.mergeTree(archiveDir, archiveDir / "usr"):
            return False
        etc = archiveDir / "usr/etc"
        if etc.exists():
            if not utils.moveFile(etc, archiveDir / "etc"):
                return False
        if not utils.createDir(self.packageDestinationDir()):
            return False
        desktopFiles = glob.glob(f"{archiveDir}/usr/share/applications/*{defines['appname']}.desktop")
        if len(desktopFiles) != 1:
            CraftCore.log.error("Failed to find the .desktop file")
            return False
        env = {"ARCH": "x86_64", "LD_LIBRARY_PATH": f"{archiveDir}/usr/lib:{archiveDir}/usr/lib/x86_64-linux-gnu"}
        if OsUtils.detectDocker:
            env["APPIMAGE_EXTRACT_AND_RUN"] = "1"
        env["OUTPUT"] = defines["setupname"]
        env["VERSION"] = self.formatVersion(includeRevision=True, includeTimeStamp=False)
        with utils.ScopedEnv(env):
            return utils.system(["linuxdeploy-x86_64.AppImage", "--appdir", self.archiveDir(), "--plugin=qt", "--output=appimage", "--desktop-file", desktopFiles[0]], cwd=self.packageDestinationDir())
