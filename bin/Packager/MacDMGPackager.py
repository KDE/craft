from Packager.CollectionPackagerBase import *
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash

import glob

class MacDMGPackager( CollectionPackagerBase ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def _setDefaults(self):
        # TODO: Fix defaults
        self.defines.setdefault("apppath", "")
        self.defines.setdefault("appname", self.package.name.lower())

    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        if not self.internalCreatePackage():
          return False

        self._setDefaults()


        archive = os.path.normpath(self.archiveDir())
        appPath = self.defines['apppath']
        if not appPath:
            apps = glob.glob(os.path.join(archive, f"**/{self.defines['appname']}.app"), recursive=True)
            if len(apps) != 1:
                CraftCore.log.error(f"Failed to detect {self.defines['appname']}.app for {self}, please provide a correct self.defines['apppath'] or a relative path to the app as self.defines['apppath']")
                return False
            appPath = apps[0]
        appPath = os.path.join(archive, appPath)
        appPath = os.path.normpath(appPath)
        CraftCore.log.info(f"Packaging {appPath}")

        targetLibdir = os.path.join(appPath, "Contents", "Frameworks")
        utils.createDir(targetLibdir)

        moveTargets = [
            (os.path.join(archive, "lib", "plugins"), os.path.join(appPath, "Contents", "PlugIns")),
            (os.path.join(archive, "plugins"), os.path.join(appPath, "Contents", "PlugIns")),
            (os.path.join(archive, "lib"), targetLibdir),
            (os.path.join(archive, "share"), os.path.join(appPath, "Contents", "Resources"))]

        if not appPath.startswith(archive):
            moveTargets += [(os.path.join(archive, "bin"), os.path.join(appPath, "Contents", "MacOS"))]

        for src, dest in moveTargets:
            if os.path.exists(src):
                if not utils.mergeTree(src, dest):
                    return False

        with utils.ScopedEnv({'DYLD_FALLBACK_LIBRARY_PATH' : os.path.join(CraftStandardDirs.craftRoot(), "lib")}):
            if not utils.system(["dylibbundler",
                                            "--overwrite-files",
                                            "--bundle-deps",
                                            "--install-path", "@executable_path/../Frameworks",
                                            "--dest-dir", targetLibdir,
                                            "--fix-file", os.path.join(appPath, "Contents", "MacOS", self.defines['appname'])]):
                return False

            if not utils.system(["macdeployqt", appPath,  "-always-overwrite", "-verbose=1"]):
                return False

            name = self.binaryArchiveName(fileType="", includeRevision=True)
            dmgDest = os.path.join(self.packageDestinationDir(), f"{name}.dmg")
            if os.path.exists(dmgDest):
                utils.deleteFile(dmgDest)
            if not utils.system(["create-dmg", "--volname", name, dmgDest, appPath]):
                return False

            CraftHash.createDigestFiles(dmgDest)

            return True
