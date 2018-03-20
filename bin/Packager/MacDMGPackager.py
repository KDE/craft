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

        self.internalCreatePackage()
        self.preArchive()

        self._setDefaults()


        archive = self.archiveDir()
        appPath = self.defines['apppath']
        if not appPath:
            apps = glob.glob(os.path.join(archive, f"**/{self.defines['appname']}.app"), recursive=True)
            if len(apps) != 1:
                CraftCore.log.error(f"Failed to detect *.app for {self}, please provide self.defines['apppath']")
                return False
            appPath = apps[0]
        appPath = os.path.join(archive, appPath)
        CraftCore.log.info(f"Packaging {appPath}")
        if os.path.exists(os.path.join(archive, "lib/plugins")):
            utils.mergeTree(os.path.join(archive, "lib/plugins"), os.path.join(appPath, "Contents/PlugIns/"))
        targetLibdir = os.path.join(appPath, "Contents/Frameworks/")
        if not os.path.exists(targetLibdir):
            os.makedirs(targetLibdir)
        if os.path.exists(os.path.join(archive, "lib")):
            utils.mergeTree(os.path.join(archive, "lib"), targetLibdir)
        if os.path.exists(os.path.join(archive, "share")):
            utils.mergeTree(os.path.join(archive, "share"), os.path.join(appPath, "Contents/Resources/"))
        utils.mergeTree(os.path.join(archive, "bin"), os.path.join(appPath, "Contents/MacOS/"))

        env = os.environ
        env['DYLD_LIBRARY_PATH'] = os.path.join(CraftStandardDirs.craftRoot(), "lib")
        if not utils.system(["dylibbundler",
                                         "--overwrite-files",
                                         "--bundle-deps",
                                         "--install-path", "@executable_path/../Frameworks",
                                         "--dest-dir", targetLibdir,
                                         "--fix-file", f"{appPath}/Contents/MacOS/{self.defines['appname']}"], env=env):
            return False

        if not utils.system(["macdeployqt", appPath,  "-always-overwrite", "-verbose=1"], env=env):
            return False

        name = self.binaryArchiveName(fileType="", includeRevision=True)
        dmgDest = os.path.join(self.packageDestinationDir(), f"{name}.dmg")
        if os.path.exists(dmgDest):
            utils.deleteFile(dmgDest)
        if not utils.system(["create-dmg", "--volname", name, dmgDest, appPath]):
            return False

        CraftHash.createDigestFiles(dmgDest)

        return True
