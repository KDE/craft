import configparser
import io
import os
import subprocess
import sys
from pathlib import Path

import utils
from CraftBase import InitGuard
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Packager.CollectionPackagerBase import CollectionPackagerBase
from Utils import CodeSign


class MacBasePackager(CollectionPackagerBase):
    @InitGuard.init_once
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.externalLibs = {}

    def internalCreatePackage(self, defines):
        """create a package"""
        CraftCore.log.debug("packaging using the MacDMGPackager")

        # TODO: provide an image with dbg files
        if not super().internalCreatePackage(defines):
            return False

        appPath = self.getMacAppPath(defines)
        if not appPath:
            return False
        archive = Path(self.archiveDir())
        CraftCore.log.info(f"Packaging {appPath}")

        CraftCore.log.info("Clean up frameworks")
        for framework in utils.filterDirectoryContent(
            archive / "lib",
            handleAppBundleAsFile=True,
            whitelist=lambda x, root: x.name.endswith(".framework"),
            blacklist=lambda x, root: True,
        ):
            rubbish = []
            framework = Path(framework)
            rubbish += framework.rglob("*.prl")
            rubbish += framework.rglob("Headers")
            for r in rubbish:
                r = Path(r)
                if r.is_symlink():
                    if framework not in r.parents:
                        raise Exception(f"Evil symlink detected: {r}")
                    utils.deleteFile(r)
                    r = r.resolve()
                if r.is_dir():
                    utils.rmtree(r)
                else:
                    utils.deleteFile(r)

        targetLibdir = os.path.join(appPath, "Contents", "Frameworks")
        utils.createDir(targetLibdir)

        moveTargets = [
            (archive / "lib/plugins", appPath / "Contents/PlugIns"),
            (archive / "plugins", appPath / "Contents/PlugIns"),
            (archive / "share", appPath / "Contents/Resources"),
            (archive / "qml", appPath / "Contents/Resources/qml"),
            (archive / "translations", appPath / "Contents/Resources/Translations"),
            (archive / "bin", appPath / "Contents/MacOS"),
            (archive / "libexec", appPath / "Contents/MacOS"),
            (archive / "lib/libexec/kf5", appPath / "Contents/MacOS"),
            (archive / "lib/libexec", appPath / "Contents/MacOS"),
            (archive / "lib", targetLibdir),
        ]
        self._addQtConf(appPath)

        if archive not in appPath.parents:
            moveTargets += [
                (
                    os.path.join(archive, "bin"),
                    os.path.join(appPath, "Contents", "MacOS"),
                )
            ]

        for src, dest in moveTargets:
            if os.path.exists(src):
                if not utils.mergeTree(src, dest):
                    return False

        dylibbundler = MacDylibBundler(appPath, self.externalLibs)
        CraftCore.log.info("Bundling main binary dependencies...")
        binaries = list(
            utils.filterDirectoryContent(
                os.path.join(appPath, "Contents"),
                whitelist=lambda x, root: utils.isBinary(x.path),
                blacklist=lambda x, root: True,
            )
        )

        for binary in binaries:
            CraftCore.log.info(f"Bundling dependencies for {binary}...")
            binaryPath = Path(binary)
            if not dylibbundler.bundleLibraryDependencies(binaryPath):
                return False

        # Finally sanity check that we don't depend on absolute paths from the builder
        CraftCore.log.info("Checking for absolute library paths in package...")
        found_bad_dylib = False  # Don't exit immeditately so that we log all the bad libraries before failing:
        for binary in binaries:
            binaryPath = Path(binary)
            if not dylibbundler.areLibraryDepsOkay(binaryPath):
                found_bad_dylib = True
                CraftCore.log.error("Found bad library dependency in binary %s", binaryPath)
        if found_bad_dylib:
            CraftCore.log.error("Cannot not create .dmg since the .app contains a bad library depenency!")
            return False
        return CodeSign.signMacApp(appPath)

    def _addQtConf(self, appFolder: Path):
        parser = configparser.ConfigParser()
        parser.optionxform = str
        parser.add_section("Paths")
        parser.set("Paths", "Imports", "Resources/qml")
        parser.set("Paths", "Qml2Imports", "Resources/qml")
        parser.set("Paths", "Translations", "Resources/Translations")
        configFile = appFolder / "Contents/Resources/qt.conf"
        utils.createDir(configFile.parent)
        with configFile.open("w", encoding="UTF-8") as conf:
            parser.write(conf)


class MacDylibBundler(object):
    """Bundle all .dylib files that are not provided by the system with the .app"""

    def __init__(self, appPath: str, externalLibs: set[str]):
        # Avoid processing the same file more than once
        self.checkedLibs = set()
        self.appPath = appPath
        self.externalLibs = externalLibs

    def _addLibToAppImage(self, libPath: Path) -> bool:
        assert libPath.is_absolute(), libPath
        if libPath in self.checkedLibs:
            return True
        # Consider only real files since symlinks are handled below
        if not libPath.exists() and not libPath.is_symlink():
            CraftCore.log.error("Library dependency '%s' does not exist", libPath)
            return False

        # Handle symlinks (such as libgit2.27.dylib -> libgit2.0.27.4.dylib):
        # Use a loop because a symlink may point to another symlink
        currentLibPath = libPath
        while currentLibPath.is_symlink():
            linkTarget = Path(os.readlink(currentLibPath))
            CraftCore.log.info("Library dependency %s is a symlink to '%s'", currentLibPath, linkTarget)
            if linkTarget.is_symlink() and linkTarget.is_absolute():
                CraftCore.log.error("%s: Cannot handle absolute symlinks: '%s'", currentLibPath, linkTarget)
                return False
            absLinkTarget = Path(os.path.join(currentLibPath.parent, linkTarget))
            # In case of symlink chains, we want to handle this only for the final target
            if not absLinkTarget.is_symlink() and not absLinkTarget.exists():
                CraftCore.log.error("Link target '%s' does not exist", linkTarget)
                return False
            if ".." in str(linkTarget):
                CraftCore.log.error(
                    "%s: Cannot handle symlinks containing '..': '%s'",
                    currentLibPath,
                    linkTarget,
                )
                return False
            if currentLibPath.resolve().parent != currentLibPath.parent.resolve():
                CraftCore.log.error(
                    "%s: Cannot handle symlinks to other directories: '%s' (%s vs %s)",
                    currentLibPath,
                    linkTarget,
                    currentLibPath.resolve().parent,
                    currentLibPath.parent.resolve(),
                )
                return False
            currentLibPath = linkTarget

        if libPath.is_symlink():
            # If the symlink target was succefully processed, the symlink itself is also fine
            return True

        CraftCore.log.debug("Handling library dependency '%s'", libPath)

        if not self._fixupLibraryId(libPath):
            return False
        for path in utils.getLibraryDeps(libPath):
            # check there aren't any references to the original location:
            if path == str(libPath):
                CraftCore.log.error(
                    "%s: failed to fix reference to original location for '%s'",
                    libPath,
                    path,
                )
                return False

        if not self.bundleLibraryDependencies(libPath):
            CraftCore.log.error(f"UNKNOWN ERROR adding '{libPath}' into bundle")
            return False
        self.checkedLibs.add(libPath)
        return True

    @staticmethod
    def _updateLibraryReferences(fileToFix: Path, changedRefs: list) -> bool:
        args = []
        for oldRef, newRef in changedRefs:
            if newRef is None:
                newRef = f"@executable_path/../Frameworks/{os.path.basename(oldRef)}"
            args += ["-change", oldRef, newRef]
        with utils.makeTemporaryWritable(fileToFix):
            if not utils.system(
                ["install_name_tool"] + args + [str(fileToFix)],
                logCommand=False,
            ):
                CraftCore.log.error("%s: failed to update library dependency paths")
                return False
        return True

    @staticmethod
    def _getLibraryNameId(fileToFix: Path) -> str:
        libraryIdOutput = io.StringIO(subprocess.check_output(["otool", "-D", str(fileToFix)]).decode("utf-8").strip())
        lines = libraryIdOutput.readlines()
        stringOutput = "".join(lines)
        if len(lines) == 1:
            return ""
        # Should have exactly one line with the id now, unless it is a universal binary
        if "arm64" in stringOutput and "x86_64" in stringOutput:
            CraftCore.log.info(f"{fileToFix} is a MacOS Intel/Silicon universal binary.")
        elif "i386" in stringOutput and "x86_64" in stringOutput:
            CraftCore.log.info(f"{fileToFix} is a 32/64 bit Intel universal binary.")
        else:
            assert len(lines) == 2, lines
        return lines[1].strip()

    @classmethod
    def _fixupLibraryId(cls, fileToFix: Path):
        libraryId = cls._getLibraryNameId(fileToFix)
        with utils.makeTemporaryWritable(fileToFix):
            if libraryId and os.path.isabs(libraryId):
                CraftCore.log.debug("Fixing library id name for %s", libraryId)
                if not utils.system(
                    [
                        "install_name_tool",
                        "-id",
                        os.path.basename(libraryId),
                        str(fileToFix),
                    ],
                    logCommand=False,
                ):
                    CraftCore.log.error("%s: failed to fix absolute library id name for", fileToFix)
                    return False
            lib = Path(CraftCore.standardDirs.craftRoot()) / "lib"
            utils.system(
                ["install_name_tool", "-delete_rpath", lib, fileToFix],
                logCommand=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                acceptableExitCodes=[0, 1],
            )
        return True

    def bundleLibraryDependencies(self, fileToFix: Path) -> bool:
        assert not fileToFix.is_symlink(), fileToFix
        if fileToFix.stat().st_nlink > 1:
            CraftCore.log.error(
                "More than one hard link to library %s found! " "This might modify another accidentally.",
                fileToFix,
            )
        CraftCore.log.info("Fixing library dependencies for %s", fileToFix)
        if not self._fixupLibraryId(fileToFix):
            return False
        # Ensure we have the current library ID since we need to skip it in the otool -L output
        libraryId = self._getLibraryNameId(fileToFix)

        changedRefs = []
        for path in utils.getLibraryDeps(str(fileToFix)):
            if path == libraryId:
                # The first line of the otool output is (usually?) the library itself:
                # $ otool -L PlugIns/printsupport/libcocoaprintersupport.dylib:
                # PlugIns/printsupport/libcocoaprintersupport.dylib:
                #         libcocoaprintersupport.dylib (compatibility version 0.0.0, current version 0.0.0)
                #         /System/Library/Frameworks/AppKit.framework/Versions/C/AppKit (compatibility version 45.0.0, current version 1561.40.112)
                #         @rpath/QtPrintSupport.framework/Versions/5/QtPrintSupport (compatibility version 5.11.0, current version 5.11.1)
                # ....
                CraftCore.log.debug(
                    "%s: ignoring library name id %s in %s",
                    fileToFix,
                    path,
                    os.path.relpath(str(fileToFix), self.appPath),
                )
                continue
            if path in self.externalLibs:
                CraftCore.log.debug("%s: allowing dependency on external library '%s'", fileToFix, path)
                continue
            if path.startswith("@executable_path/"):
                continue  # already fixed
            if path.startswith("@rpath/"):
                changedRefs.append((path, "@executable_path/../Frameworks/" + path[len("@rpath/") :]))
            elif path.startswith("/usr/lib/") or path.startswith("/System/Library/Frameworks/"):
                CraftCore.log.debug("%s: allowing dependency on system library '%s'", fileToFix, path)
            elif path.startswith("@loader_path/"):
                CraftCore.log.debug(f"{fileToFix}: Accept '{path}' into.")
            else:
                guessedNewRef = None
                if path.startswith(str(CraftStandardDirs.craftRoot() / "lib")):
                    guessedPath = path.replace(
                        str(CraftStandardDirs.craftRoot() / "lib"),
                        os.path.join(self.appPath, "Contents/Frameworks"),
                    )
                    # Update possible new ref for deps in framework
                    if f"{os.path.basename(guessedPath)}.framework" in guessedPath:
                        guessedNewRef = path.replace(
                            str(CraftStandardDirs.craftRoot() / "lib"),
                            "@executable_path/../Frameworks/",
                        )
                elif not path.startswith("/"):
                    guessedPath = os.path.join(self.appPath, "Contents/Frameworks", path)
                else:
                    CraftCore.log.error(
                        "%s: don't know how to handle otool -L output: '%s'",
                        fileToFix,
                        path,
                    )
                    return False
                if not self._addLibToAppImage(Path(guessedPath)):
                    CraftCore.log.error(f"{fileToFix}: Failed to add library dependency '{guessedPath}' into bundle")
                    return False
                changedRefs.append((path, guessedNewRef))

        if changedRefs:
            if not self._updateLibraryReferences(fileToFix, changedRefs):
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
            if dep.startswith("/usr/lib/") or dep.startswith("/System/Library/Frameworks/") or dep in self.externalLibs:
                continue
            if dep.startswith(CraftStandardDirs.craftRoot()):
                CraftCore.log.error(
                    "ERROR: %s references absolute library path from craftroot: %s",
                    relativePath,
                    dep,
                )
            elif dep.startswith("/"):
                CraftCore.log.error("ERROR: %s references absolute library path: %s", relativePath, dep)
            else:
                CraftCore.log.error("ERROR: %s has bad dependency: %s", relativePath, dep)
            found_bad_lib = True
        return not found_bad_lib


if __name__ == "__main__":
    print("Testing MacDMGPackager.py")
    defaultFile = f"{CraftStandardDirs.craftRoot()}/lib/libKF5TextEditor.5.dylib"
    sourceFile = defaultFile if len(sys.argv) else sys.argv[1]
    utils.system(["otool", "-L", sourceFile])
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        source = os.path.realpath(sourceFile)
        target = os.path.join(td, os.path.basename(source))
        utils.copyFile(source, target, linkOnly=False)
        bundler = MacDylibBundler(td, {})
        bundler.bundleLibraryDependencies(Path(target))
        print("Checked libs:", bundler.checkedLibs)
        utils.system(["find", td])
        utils.system(["ls", "-laR", td])
        if not bundler.areLibraryDepsOkay(Path(target)):
            print("Error")
        # utils.system(["find", td, "-type", "f", "-execdir", "otool", "-L", "{}", ";"])
