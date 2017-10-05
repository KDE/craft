from Packager.CollectionPackagerBase import *

class MacDMGPackager( CollectionPackagerBase ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        self.internalCreatePackage()
        self.preArchive()

        archive = self.archiveDir()
        appPath = os.path.join(archive, "Applications/KDE/kdevelop.app")
        utils.mergeTree(os.path.join(archive, "lib/plugins"), os.path.join(appPath, "Contents/PlugIns/"))
        targetLibdir = os.path.join(appPath, "Contents/Frameworks/")
        if not os.path.exists(targetLibdir):
            os.mkdir(targetLibdir)
        utils.mergeTree(os.path.join(archive, "lib"), targetLibdir)
        utils.mergeTree(os.path.join(archive, "share"), os.path.join(appPath, "Contents/Resources/"))
        utils.mergeTree(os.path.join(archive, "bin"), os.path.join(appPath, "Contents/MacOS/"))

        env = os.environ
        env['DYLD_LIBRARY_PATH'] = os.path.join(CraftStandardDirs.craftRoot(), "lib")
        if not utils.systemWithoutShell(["dylibbundler", "-of", "-b", "-p", "@executable_path/../Frameworks", "-d", targetLibdir, "-x", f"{appPath}/Contents/MacOS/kdevelop"], env=env):
            CraftCore.log.warning("Failed to run dylibbundler")

        if not utils.systemWithoutShell(["macdeployqt", appPath,  "-always-overwrite", "-dmg", "-verbose=2"], env=env):
            CraftCore.log.warning("Failed to run macdeployqt!")

        return True
