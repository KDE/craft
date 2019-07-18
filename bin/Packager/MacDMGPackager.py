from Packager.CollectionPackagerBase import *
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash
from pathlib import Path
import contextlib
import io
import subprocess
import stat
import glob


class MacDMGPackager( CollectionPackagerBase ):

    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__(self, whitelists, blacklists)

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        defines["setupname"] = str(Path(defines["setupname"]).with_suffix(".dmg"))
        return defines

    def createPackage(self):
        """ create a package """
        CraftCore.log.debug("packaging using the MacDMGPackager")

        defines = self.setDefaults(self.defines)
        # TODO: provide an image with dbg files
        if not self.internalCreatePackage(defines, False):
            return False

        appPath = self.getMacAppPath(defines)
        archive = os.path.normpath(self.archiveDir())
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

        dylibbundler = MacDylibBundler(appPath)
        with utils.ScopedEnv({'DYLD_FALLBACK_LIBRARY_PATH': targetLibdir + ":" + os.path.join(CraftStandardDirs.craftRoot(), "lib")}):
            CraftCore.log.info("Bundling main binary dependencies...")
            mainBinary = Path(appPath, "Contents", "MacOS", defines['appname'])
            if not dylibbundler.bundleLibraryDependencies(mainBinary):
                return False

            binaries = list(utils.filterDirectoryContent(os.path.join(appPath, "Contents", "MacOS"),
                                                         whitelist=lambda x, root: utils.isBinary(os.path.join(root, x)) and x.name != defines["appname"],
                                                         blacklist=lambda x, root: x.name == defines["appname"]))

            for binary in binaries:
                CraftCore.log.info(f"Bundling dependencies for {binary}...")
                binaryPath = Path(binary)
                if not dylibbundler.bundleLibraryDependencies(binaryPath):
                    return False

            # Fix up the library dependencies of files in Contents/Frameworks/
            CraftCore.log.info("Bundling library dependencies...")
            if not dylibbundler.fixupAndBundleLibsRecursively("Contents/Frameworks"):
                return False
            CraftCore.log.info("Bundling plugin dependencies...")
            if not dylibbundler.fixupAndBundleLibsRecursively("Contents/PlugIns"):
                return False

            macdeployqt_multiple_executables_command = ["macdeployqt", appPath, "-always-overwrite", "-verbose=1"]
            for binary in binaries:
                macdeployqt_multiple_executables_command.append(f"-executable={binary}")
            if not utils.system(macdeployqt_multiple_executables_command):
                return False

            # macdeployqt might just have added some explicitly blacklisted files
            blackList = Path(self.packageDir(), "mac_blacklist.txt")
            if blackList.exists():
                pattern = [self.read_blacklist(str(blackList))]
                # use it as whitelist as we want only matches, ignore all others
                matches = utils.filterDirectoryContent(appPath, whitelist=lambda x, root: utils.regexFileFilter(x, root, pattern), blacklist=lambda x, root:True)
                for f in matches:
                    CraftCore.log.info(f"Remove blacklisted file: {f}")
                    utils.deleteFile(f)

            # macdeployqt adds some more plugins so we fix the plugins after calling macdeployqt
            dylibbundler.checkedLibs = set()  # ensure we check all libs again (but
            # we should not need to make any changes)
            CraftCore.log.info("Fixing plugin dependencies after macdeployqt...")
            if not dylibbundler.fixupAndBundleLibsRecursively("Contents/PlugIns"):
                return False
            CraftCore.log.info("Fixing library dependencies after macdeployqt...")
            if not dylibbundler.fixupAndBundleLibsRecursively("Contents/Frameworks"):
                return False

            # Finally sanity check that we don't depend on absolute paths from the builder
            CraftCore.log.info("Checking for absolute library paths in package...")
            found_bad_dylib = False  # Don't exit immeditately so that we log all the bad libraries before failing:
            if not dylibbundler.areLibraryDepsOkay(mainBinary):
                found_bad_dylib = True
                CraftCore.log.error("Found bad library dependency in main binary %s", mainBinary)
            for binary in binaries:
                binaryPath = Path(binary)
                if not dylibbundler.areLibraryDepsOkay(binaryPath):
                    found_bad_dylib = True
                    CraftCore.log.error("Found bad library dependency in binary %s", binaryPath)
            if not dylibbundler.checkLibraryDepsRecursively("Contents/Frameworks"):
                CraftCore.log.error("Found bad library dependency in bundled libraries")
                found_bad_dylib = True
            if not dylibbundler.checkLibraryDepsRecursively("Contents/PlugIns"):
                CraftCore.log.error("Found bad library dependency in bundled plugins")
                found_bad_dylib = True
            if found_bad_dylib:
                CraftCore.log.error("Cannot not create .dmg since the .app contains a bad library depenency!")
                return False

            dmgDest = defines["setupname"]
            if os.path.exists(dmgDest):
                utils.deleteFile(dmgDest)
            appName = defines['appname'] + ".app"
            if not utils.system(["create-dmg", "--volname", os.path.basename(dmgDest),
                                 # Add a drop link to /Applications:
                                 "--icon", appName, "140", "150", "--app-drop-link", "350", "150",
                                 dmgDest, appPath]):
                return False

            CraftHash.createDigestFiles(dmgDest)

            return True

class MacDylibBundler(object):
    """ Bundle all .dylib files that are not provided by the system with the .app """
    def __init__(self, appPath: str):
        # Avoid processing the same file more than once
        self.checkedLibs = set()
        self.appPath = appPath

    def _addLibToAppImage(self, libPath: Path) -> bool:
        assert libPath.is_absolute(), libPath
        libBasename = libPath.name
        targetPath = Path(self.appPath, "Contents/Frameworks/", libBasename)
        if targetPath.exists() and targetPath in self.checkedLibs:
            return True
        # Handle symlinks (such as libgit2.27.dylib -> libgit2.0.27.4.dylib):
        if libPath.is_symlink():
            linkTarget = os.readlink(str(libPath))
            CraftCore.log.info("Library dependency %s is a symlink to '%s'", libPath, linkTarget)
            if os.path.isabs(linkTarget):
                CraftCore.log.error("%s: Cannot handle absolute symlinks: '%s'", libPath, linkTarget)
                return False
            if ".." in linkTarget:
                CraftCore.log.error("%s: Cannot handle symlinks containing '..': '%s'", libPath, linkTarget)
                return False
            if libPath.resolve().parent != libPath.parent.resolve():
                CraftCore.log.error("%s: Cannot handle symlinks to other directories: '%s' (%s vs %s)",
                                    libPath, linkTarget, libPath.resolve().parent, libPath.parent.resolve())
                return False

            # copy the symlink and add the real file:
            utils.copyFile(str(libPath), str(targetPath), linkOnly=False)
            CraftCore.log.info("Added symlink '%s' (%s) to bundle -> %s", libPath,
                               os.readlink(str(targetPath)), targetPath)
            self.checkedLibs.add(targetPath)
            symlinkTarget = libPath.with_name(os.path.basename(linkTarget))
            CraftCore.log.info("Processing symlink target '%s'", symlinkTarget)
            if not self._addLibToAppImage(symlinkTarget):
                self.checkedLibs.remove(targetPath)
                return False
            # If the symlink target was processed, the symlink itself is also fine
            return True

        if not libPath.exists():
            CraftCore.log.error("Library dependency '%s' does not exist", libPath)
            return False
        CraftCore.log.debug("Handling library dependency '%s'", libPath)
        if not targetPath.exists():
            utils.copyFile(str(libPath), str(targetPath), linkOnly=False)
            CraftCore.log.info("Added library dependency '%s' to bundle -> %s", libPath, targetPath)

        if not self._fixupLibraryId(targetPath):
            return False
        for path in utils.getLibraryDeps(str(targetPath)):
            # check there aren't any references to the original location:
            if path == str(libPath):
                CraftCore.log.error("%s: failed to fix reference to original location for '%s'", targetPath, path)
                return False

        if not self.bundleLibraryDependencies(targetPath):
            CraftCore.log.error("%s: UNKNOWN ERROR adding '%s' into bundle", targetPath, libPath)
            return False
        if not os.path.exists(targetPath):
            CraftCore.log.error("%s: Library dependency '%s' doesn't exist after copying... Symlink error?",
                                targetPath, libPath)
            return False
        self.checkedLibs.add(targetPath)
        return True

    @staticmethod
    def _updateLibraryReference(fileToFix: Path, oldRef: str, newRef: str = None) -> bool:
        if newRef is None:
            newRef = "@executable_path/../Frameworks/" + os.path.basename(oldRef)
        with utils.makeWritable(fileToFix):
            if not utils.system(["install_name_tool", "-change", oldRef, newRef, str(fileToFix)], logCommand=False):
                CraftCore.log.error("%s: failed to update library dependency path from '%s' to '%s'",
                                    fileToFix, oldRef, newRef)
                return False
        return True

    @staticmethod
    def _getLibraryNameId(fileToFix: Path) -> str:
        libraryIdOutput = io.StringIO(
            subprocess.check_output(["otool", "-D", str(fileToFix)]).decode("utf-8").strip())
        lines = libraryIdOutput.readlines()
        if len(lines) == 1:
            return ""
        # Should have exactly one line with the id now
        assert len(lines) == 2, lines
        return lines[1].strip()

    @classmethod
    def _fixupLibraryId(cls, fileToFix: Path):
        libraryId = cls._getLibraryNameId(fileToFix)
        if libraryId and os.path.isabs(libraryId):
            CraftCore.log.debug("Fixing library id name for %s", libraryId)
            with utils.makeWritable(fileToFix):
                if not utils.system(["install_name_tool", "-id", os.path.basename(libraryId), str(fileToFix)],
                                    logCommand=False):
                    CraftCore.log.error("%s: failed to fix absolute library id name for", fileToFix)
                    return False
        return True

    def bundleLibraryDependencies(self, fileToFix: Path) -> bool:
        assert not fileToFix.is_symlink(), fileToFix
        if fileToFix.stat().st_nlink > 1:
            CraftCore.log.error("More than one hard link to library %s found! "
                                "This might modify another accidentally.", fileToFix)
        CraftCore.log.info("Fixing library dependencies for %s", fileToFix)
        if not self._fixupLibraryId(fileToFix):
            return False
        # Ensure we have the current library ID since we need to skip it in the otool -L output
        libraryId = self._getLibraryNameId(fileToFix)

        for path in utils.getLibraryDeps(str(fileToFix)):
            if path == libraryId:
                # The first line of the otool output is (usually?) the library itself:
                # $ otool -L PlugIns/printsupport/libcocoaprintersupport.dylib:
                # PlugIns/printsupport/libcocoaprintersupport.dylib:
                #         libcocoaprintersupport.dylib (compatibility version 0.0.0, current version 0.0.0)
                #         /System/Library/Frameworks/AppKit.framework/Versions/C/AppKit (compatibility version 45.0.0, current version 1561.40.112)
                #         @rpath/QtPrintSupport.framework/Versions/5/QtPrintSupport (compatibility version 5.11.0, current version 5.11.1)
                # ....
                CraftCore.log.debug("%s: ignoring library name id %s in %s", fileToFix, path,
                                    os.path.relpath(str(fileToFix), self.appPath))
                continue
            if path.startswith("@executable_path/"):
                continue  # already fixed
            if path.startswith("@rpath/"):
                # CraftCore.log.info("%s: can't handle @rpath library dep of yet: '%s'", fileToFix, path)
                CraftCore.log.debug("%s: can't handle @rpath library dep of yet: '%s'", fileToFix, path)
                # TODO: run otool -l and verify that we pick the right file?
            elif path.startswith("/usr/lib/") or path.startswith("/System/Library/Frameworks/"):
                CraftCore.log.debug("%s: allowing dependency on system library '%s'", fileToFix, path)
            elif path.startswith("/"):
                if not path.startswith(CraftStandardDirs.craftRoot()):
                    CraftCore.log.error("%s: reference to absolute library path outside craftroot: %s",
                                          fileToFix, path)
                    return False
                # file installed by craft -> bundle it into the .app if it doesn't exist yet
                if not self._addLibToAppImage(Path(path)):
                    CraftCore.log.error(f"{fileToFix}: Failed to add library dependency '{path}' into bundle")
                    return False
                if not self._updateLibraryReference(fileToFix, path):
                    return False
            elif "/" not in path and path.startswith("lib"):
                # library reference without absolute path -> try to find the library
                # First check if it exists in Contents/Frameworks already
                guessedPath = Path(self.appPath, "Frameworks", path)
                if guessedPath.exists():
                    CraftCore.log.info("%s: relative library dependency is alreayd bundled: %s", fileToFix, guessedPath)
                else:
                    guessedPath = Path(CraftStandardDirs.craftRoot(), "lib", path)
                    if not guessedPath.exists():
                        CraftCore.log.error("%s: Could not find library dependency '%s' in craftroot", fileToFix, path)
                        return False
                CraftCore.log.debug("%s: Found relative library reference %s in '%s'", fileToFix, path, guessedPath)
                if not self._addLibToAppImage(guessedPath):
                    CraftCore.log.error("%s: Failed to add library dependency '%s' into bundle", fileToFix,
                                        guessedPath)
                    return False
                if not self._updateLibraryReference(fileToFix, path):
                    return False
            elif path.startswith("@loader_path/"):
                CraftCore.log.debug(f"{fileToFix}: Accept '{path}' into.")
            else:
                CraftCore.log.error("%s: don't know how to handle otool -L output: '%s'", fileToFix, path)
                return False
        return True

    def fixupAndBundleLibsRecursively(self, subdir: str):
        """Remove absolute references and budle all depedencies for all dylibs under :p subdir"""
        assert not subdir.startswith("/"), "Must be a relative path"
        for dirpath, dirs, files in os.walk(os.path.join(self.appPath, subdir)):
            for filename in files:
                fullpath = Path(dirpath, filename)
                if fullpath.is_symlink():
                    continue  # No need to update symlinks since we will process the target eventually.
                if (filename.endswith(".so")
                        or filename.endswith(".dylib")
                        or ".so." in filename
                        or (f"{fullpath.name}.framework" in str(fullpath) and utils.isBinary(str(fullpath)))):
                    if not self.bundleLibraryDependencies(fullpath):
                        CraftCore.log.info("Failed to bundle dependencies for '%s'", os.path.join(dirpath, filename))
                        return False
        return True

    def areLibraryDepsOkay(self, fullPath: Path):
        CraftCore.log.debug("Checking library dependencies of %s", fullPath)
        found_bad_lib = False
        libraryId = self._getLibraryNameId(fullPath)
        relativePath = os.path.relpath(str(fullPath), self.appPath)
        for dep in utils.getLibraryDeps(str(fullPath)):
            if dep == libraryId and not os.path.isabs(libraryId):
                continue  # non-absolute library id is fine
            # @rpath and @executable_path is fine
            if dep.startswith("@rpath") or dep.startswith("@executable_path") or dep.startswith("@loader_path"):
                continue
            # Also allow /System/Library/Frameworks/ and /usr/lib:
            if dep.startswith("/usr/lib/") or dep.startswith("/System/Library/Frameworks/"):
                continue
            if dep.startswith(CraftStandardDirs.craftRoot()):
                CraftCore.log.error("ERROR: %s references absolute library path from craftroot: %s", relativePath,
                                    dep)
            elif dep.startswith("/"):
                CraftCore.log.error("ERROR: %s references absolute library path: %s", relativePath, dep)
            else:
                CraftCore.log.error("ERROR: %s has bad dependency: %s", relativePath, dep)
            found_bad_lib = True
        return not found_bad_lib

    def checkLibraryDepsRecursively(self, subdir: str):
        """Check that all  absolute references and budle all depedencies for all dylibs under :p subdir"""
        assert not subdir.startswith("/"), "Must be a relative path"
        foundError = False
        for dirpath, dirs, files in os.walk(os.path.join(self.appPath, subdir)):
            for filename in files:
                fullpath = Path(dirpath, filename)
                if fullpath.is_symlink() and not fullpath.exists():
                    CraftCore.log.error("Found broken symlink '%s' (%s)", fullpath,
                                        os.readlink(str(fullpath)))
                    foundError = True
                    continue

                if filename.endswith(".so") or filename.endswith(".dylib") or ".so." in filename:
                    if not self.areLibraryDepsOkay(fullpath):
                        CraftCore.log.error("Found library dependency error in '%s'", fullpath)
                        foundError = True
        return not foundError


if __name__ == '__main__':
    print("Testing MacDMGPackager.py")
    defaultFile = CraftStandardDirs.craftRoot() + "/lib/libKF5TextEditor.5.dylib"
    sourceFile = defaultFile if len(sys.argv) else sys.argv[1]
    utils.system(["otool", "-L", sourceFile])
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        source = os.path.realpath(sourceFile)
        target = os.path.join(td, os.path.basename(source))
        utils.copyFile(source, target, linkOnly=False)
        bundler = MacDylibBundler(td)
        bundler.bundleLibraryDependencies(Path(target))
        print("Checked libs:", bundler.checkedLibs)
        utils.system(["find", td])
        utils.system(["ls", "-laR", td])
        if not bundler.areLibraryDepsOkay(Path(target)):
            print("Error")
        if not bundler.checkLibraryDepsRecursively("Contents/Frameworks"):
            print("Error 2")
        # utils.system(["find", td, "-type", "f", "-execdir", "otool", "-L", "{}", ";"])
