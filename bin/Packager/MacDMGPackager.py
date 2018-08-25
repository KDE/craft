from Packager.CollectionPackagerBase import *
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash
import io
import subprocess

import glob


class MacDMGPackager( CollectionPackagerBase ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def _setDefaults(self):
        # TODO: Fix defaults
        self.defines.setdefault("apppath", "")
        self.defines.setdefault("appname", self.package.name.lower())

    @staticmethod
    def _getLibraryDeps(fullPath):
        lines = io.StringIO(subprocess.check_output(["otool", "-L", fullPath]).decode("utf-8"))
        deps = []
        for line in lines:
            if line.startswith("\t"):
                deps.append(line.strip())
        return deps

    def areLibraryDepsOkay(self, fullPath, relativePath):
        CraftCore.log.debug("Checking library dependencies of %s", fullPath)
        found_bad_lib = False
        for dep in self._getLibraryDeps(fullPath):
            # @rpath and @executable_path is fine
            if dep.startswith("@rpath") or dep.startswith("@executable_path"):
                continue
            # Also allow /System/Library/Frameworks/ and /usr/lib:
            if dep.startswith("/usr/lib/") or dep.startswith("/System/Library/Frameworks/"):
                continue
            if dep.startswith(CraftStandardDirs.craftRoot()):
                CraftCore.log.error("ERROR: %s references absolute library path from craftroot: %s", relativePath, dep)
            elif dep.startswith("/"):
                CraftCore.log.error("ERROR: %s references absolute library path: %s", relativePath, dep)
            found_bad_lib = True
        return not found_bad_lib

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

        with utils.ScopedEnv({'DYLD_FALLBACK_LIBRARY_PATH': targetLibdir + ":" + os.path.join(CraftStandardDirs.craftRoot(), "lib")}):
            CraftCore.log.info("Checking for absolute library paths...")
            binaryDir = os.path.join(appPath, "Contents", "MacOS")
            mainBinary = os.path.join(binaryDir, self.defines['appname'])
            if not utils.system(["dylibbundler",
                                            "--overwrite-files",
                                            "--bundle-deps",
                                            "--install-path", "@executable_path/../Frameworks",
                                            "--dest-dir", targetLibdir,
                                            "--fix-file", mainBinary]):
                return False

            # Finally sanity check that we don't depend on absolute paths from the builder
            CraftCore.log.info("Checking for absolute library paths in package...")
            found_bad_dylib = False
            if not self.areLibraryDepsOkay(mainBinary, self.defines['appname']):
                # Don't return false here so that we log all the bad libraries before failing:
                found_bad_dylib = True
            for dirpath, dirnames, filenames in os.walk(os.path.join(appPath, "Contents", "PlugIns")):
                for filename in filenames:
                    # TODO: check for Mach-O file magic instead of filtering by name:
                    fullpath = os.path.join(dirpath, filename)
                    if not self.areLibraryDepsOkay(fullpath, os.path.relpath(fullpath, appPath)):
                        found_bad_dylib = True
                    break
            if found_bad_dylib:
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
