# -*- coding: utf-8 -*-
# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Ralf Habacker <ralf.habacker [AT] freenet [DOT] de>
# Copyright Hannah von Reth <vonreth@kde.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import configparser
import contextlib
import ctypes
import glob
import io
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Optional

import Notifier.NotificationLoader
from CraftCore import CraftCore
from CraftDebug import deprecated
from CraftOS.osutils import OsUtils
from Utils.Arguments import Arguments
from Utils.Dos2UnixFile import Dos2UnixFile
from Utils.StageLogger import StageLogger


def __locate7z():
    app = CraftCore.cache.findApplication("7za")
    if app:
        return app
    appPath = CraftCore.standardDirs.craftRoot() / "dev-utils/7z" / ("7za.exe" if CraftCore.compiler.isWindows else "7zz")
    if appPath.exists():
        return appPath
    return None


# unpack functions


def unpackFiles(downloaddir, filenames, workdir):
    """unpack (multiple) files specified by 'filenames' from 'downloaddir' into 'workdir'"""

    for filename in filenames:
        if not unpackFile(downloaddir, filename, workdir):
            return False

    return True


def unpackFile(downloaddir, filename, workdir, keepSymlinksOnWindows=True, sevenZipExtraArgs=[]):
    """unpack file specified by 'filename' from 'downloaddir' into 'workdir'"""
    CraftCore.log.debug(f"unpacking this file: {filename}")
    if not filename:
        return True

    (shortname, ext) = os.path.splitext(filename)
    if ext == "":
        CraftCore.log.warning(f"unpackFile called on invalid file extension {filename}")
        return True

    if OsUtils.isWin() and not OsUtils.supportsSymlinks():
        CraftCore.log.warning(
            "Please enable Windows 10 development mode to enable support for symlinks.\n"
            "This will enable faster extractions.\n"
            "https://docs.microsoft.com/en-us/windows/uwp/get-started/enable-your-device-for-development"
        )
    if __locate7z():
        # we use tar on linux not 7z, don't use tar on windows as it skips symlinks
        # test it with breeze-icons
        if (
            not OsUtils.isWin()
            or (OsUtils.supportsSymlinks() and CraftCore.cache.getVersion(__locate7z(), versionCommand="-version") >= "16")
            or not re.match(r"(.*\.tar.*$|.*\.tgz$)", filename)
        ):
            return un7zip(os.path.join(downloaddir, filename), workdir, ext, keepSymlinksOnWindows=keepSymlinksOnWindows, extraArgs=sevenZipExtraArgs)
    try:
        shutil.unpack_archive(os.path.join(downloaddir, filename), workdir)
    except Exception as e:
        CraftCore.log.error(f"Failed to unpack {filename}", exc_info=e)
        return False
    return True


def un7zip(fileName, destdir, flag=None, keepSymlinksOnWindows=True, extraArgs=[]):
    ciMode = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)
    createDir(destdir)
    kw = {}
    progressFlags = []
    type = []
    app = __locate7z()
    if not ciMode and CraftCore.cache.checkCommandOutputFor(app, "-bs"):
        progressFlags = ["-bso2", "-bsp1"]
        kw["stderr"] = subprocess.PIPE

    if flag == ".7z":
        # Actually this is not needed for a normal archive.
        # But git is an exe file renamed to 7z and we need to specify the type.
        # Yes it is an ugly hack.
        type = ["-t7z"]
    if re.match(r"(.*\.tar.*$|.*\.tgz$)", fileName):
        if progressFlags:
            if ciMode:
                progressFlags = []
            else:
                # print progress to stderr
                progressFlags = ["-bsp2"]
        kw["pipeProcess"] = subprocess.Popen([app, "x", fileName, "-so"] + extraArgs + progressFlags, stdout=subprocess.PIPE)
        if CraftCore.compiler.isWindows:
            if progressFlags:
                progressFlags = ["-bsp0"]
            command = [app, "x", "-si", f"-o{destdir}", "-ttar"] + extraArgs + progressFlags
            kw["stdout"] = subprocess.DEVNULL
        else:
            tar = CraftCore.cache.findApplication("tar")
            command = [tar, "--directory", destdir, "-xf", "-"]
    else:
        command = [app, "x", "-r", "-y", f"-o{destdir}", fileName] + type + extraArgs + progressFlags

    # While 7zip supports symlinks cmake 3.8.0 does not support symlinks
    if not system(command, **kw):
        return False
    if CraftCore.compiler.isWindows and not keepSymlinksOnWindows:
        return replaceSymlinksWithCopies(destdir)
    return True


def compress(archive: Path, source: str) -> bool:
    archive = Path(archive)
    ciMode = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)

    def __7z(archive, source):
        app = __locate7z()
        kw = {}
        flags = []
        if archive.suffix in {".appxsym", ".appxupload"}:
            flags.append("-tzip")
        if not ciMode and CraftCore.cache.checkCommandOutputFor(app, "-bs"):
            flags += ["-bso2", "-bsp1"]
            kw["stderr"] = subprocess.PIPE
        if str(archive).endswith(".tar.7z"):
            tar = CraftCore.cache.findApplication("tar")
            kw["pipeProcess"] = subprocess.Popen(
                [
                    tar,
                    "-cf",
                    "-",
                    "-C",
                    source,
                    ".",
                ],
                stdout=subprocess.PIPE,
            )
            command = [app, "a", "-si", archive] + flags
        else:
            command = [app, "a", "-r", archive] + flags

        if isinstance(source, list):
            command += source
        elif os.path.isfile(source):
            command += [source]
        else:
            command += [os.path.join(source, "*")]
        return system(command, displayProgress=True, **kw)

    def __xz(archive, source):
        command = ["tar", "-cJf", archive, "-C"]
        if os.path.isfile(source):
            command += [source]
        else:
            command += [source, "."]
        return system(command)

    createDir(os.path.dirname(archive))
    if os.path.isfile(archive):
        deleteFile(archive)

    if not __locate7z() and archive.suffix == ".zip":
        return shutil.make_archive(archive.with_suffix(""), "zip", source)

    if CraftCore.compiler.isUnix and archive.suffixes[-2:] == [".tar", ".xz"]:
        return __xz(archive, source)
    else:
        return __7z(archive, source)


def system(cmd, displayProgress=False, logCommand=True, acceptableExitCodes=None, **kw):
    """execute cmd in a shell. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options."""
    return systemWithoutShell(
        cmd,
        displayProgress=displayProgress,
        logCommand=logCommand,
        acceptableExitCodes=acceptableExitCodes,
        **kw,
    )


def systemWithoutShell(
    cmd,
    displayProgress=False,
    logCommand=True,
    pipeProcess=None,
    acceptableExitCodes=None,
    secretCommand=False,
    secret=None,
    outputOnFailure=None,
    **kw,
):
    """execute cmd. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options.

    When the parameter "displayProgress" is True, stdout won't be
    logged to allow the display of progress bars."""

    ciMode = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)
    needsAnsiFix = OsUtils.isWin() and CraftCore.settings.getboolean("General", "AllowAnsiColor", True)
    if outputOnFailure is None:
        outputOnFailure = StageLogger.isOutputOnFailure()

    def ansiFix():
        if needsAnsiFix:
            # a bug in cygwin msys removes the ansi flag, set it again
            ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
            ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-12), 7)

    environment = kw.get("env", os.environ)
    cwd = kw.get("cwd", os.getcwd())
    acceptableExitCodes = acceptableExitCodes or [0]

    # make sure our venv python is used
    python_venv = Path(CraftCore.standardDirs.etcDir()) / f"virtualenv/3/Scripts/python{CraftCore.compiler.executableSuffix}"
    if python_venv.exists():
        environment["VIRTUAL_ENV"] = str(python_venv.parent)

    # if the first argument is not an absolute path replace it with the full path to the application
    if isinstance(cmd, Arguments):
        cmd = Arguments.get(cmd)

    if isinstance(cmd, list):
        # allow to pass other types, like ints or Path
        cmd = [str(x) for x in cmd]
        if pipeProcess:
            pipeProcess.args = [str(x) for x in pipeProcess.args]
        arg0 = cmd[0]
        if "shell" not in kw:
            kw["shell"] = False
    else:
        if "shell" not in kw:
            # use shell, arg0 might end up with "/usr/bin/svn" => needs shell so it can be executed
            kw["shell"] = True
        arg0 = shlex.split(cmd, posix=not OsUtils.isWin())[0]

    matchQuoted = re.match('^"(.*)"$', arg0)
    if matchQuoted:
        CraftCore.log.warning(f"Please don't pass quoted paths to systemWithoutShell, app={arg0}")
    if not os.path.isfile(arg0) and not matchQuoted:
        app = CraftCore.cache.findApplication(arg0)
    else:
        app = arg0

    if app:
        if isinstance(cmd, list):
            cmd[0] = app
        elif not matchQuoted:
            cmd = cmd.replace(arg0, f'"{app}"', 1)
    else:
        app = arg0

    if secretCommand:
        CraftCore.debug.print(f"securely executing command: {app}")
    else:
        _logCommand = ""
        _debugCommand = ""
        if logCommand:
            if pipeProcess:
                _logCommand = "{0} | ".format(" ".join(pipeProcess.args))
            _logCommand += " ".join([str(c) for c in cmd]) if isinstance(cmd, list) else cmd
        if pipeProcess:
            _debugCommand = f"executing command: {pipeProcess.args!r} | {cmd!r}"
        else:
            _debugCommand = f"executing command: {cmd!r}"
        if secret:
            _debugCommand = redact(_debugCommand, secret)
            _logCommand = redact(_logCommand, secret)
        if logCommand and not StageLogger.isOutputOnFailure():
            CraftCore.debug.print(f"executing command: {_logCommand}")
        StageLogger.logLine(f"executing command: {_debugCommand}")
        CraftCore.log.debug(_debugCommand)
        CraftCore.log.debug(f"CWD: {cwd!r}")
        CraftCore.log.debug(f"displayProgress={displayProgress}")
        CraftCore.debug.logEnv(environment)
    if pipeProcess:
        kw["stdin"] = pipeProcess.stdout
    if not displayProgress or ciMode:
        stdout = kw.get("stdout", sys.stdout)
        if stdout == sys.stdout:
            kw["stderr"] = subprocess.STDOUT
        kw["stdout"] = subprocess.PIPE

        proc = subprocess.Popen(cmd, **kw)
        if pipeProcess:
            pipeProcess.stdout.close()
        for line in proc.stdout:
            lineUtf8 = line.decode("utf-8", errors="backslashreplace")
            StageLogger.log(lineUtf8)
            if isinstance(stdout, io.TextIOWrapper):
                if not outputOnFailure and CraftCore.debug.verbose() < 3:  # don't print if we write the debug log to stdout anyhow
                    ansiFix()
                    stdout.buffer.write(line)
                    stdout.flush()
            elif stdout == subprocess.DEVNULL:
                pass
            elif isinstance(stdout, io.TextIOBase) or "IORedirector" in stdout.__class__.__name__:
                stdout.write(lineUtf8)
            else:
                stdout.write(line)

            CraftCore.log.debug("{app}: {out}".format(app=app, out=line.rstrip()))
    else:
        proc = subprocess.Popen(cmd, **kw)
        if pipeProcess:
            pipeProcess.stdout.close()
        if proc.stderr:
            for line in proc.stderr:
                CraftCore.log.debug("{app}: {out}".format(app=app, out=line.rstrip()))

    proc.communicate()
    proc.wait()

    # if there was no output
    ansiFix()

    if proc.returncode in acceptableExitCodes:
        resultMessage = f"Command {redact(cmd, secret)} succeeded with exit code {proc.returncode}"
        StageLogger.logLine(resultMessage)
        if not outputOnFailure:
            if proc.returncode == 0:
                CraftCore.log.debug(resultMessage)
            else:
                CraftCore.log.info(resultMessage)
        return True
    resultMessage = f"Command {redact(cmd, secret)} failed with exit code {proc.returncode}"
    StageLogger.logLine(resultMessage)
    if not outputOnFailure:
        CraftCore.log.info(resultMessage)
    return False


def cleanDirectory(directory):
    CraftCore.log.debug("clean directory %s" % directory)
    if os.path.exists(directory):
        # don't delete containg directrory as it might be a symlink and replacing it with a folder
        # breaks the behaviour
        with os.scandir(directory) as scan:
            for f in scan:
                if f.is_dir():
                    if not OsUtils.rmDir(f.path, force=True):
                        return False
                else:
                    if not OsUtils.rm(f.path, force=True):
                        return False
        return True
    else:
        return createDir(directory)


def getVCSType(url):
    """return the type of the vcs url"""
    if not url:
        return ""
    if isGitUrl(url):
        return "git"
    elif isSvnUrl(url):
        return "svn"
    elif url.startswith("[hg]"):
        return "hg"
    # \todo complete more cvs access schemes
    elif url.find("pserver:") >= 0:
        return "cvs"
    else:
        return "git"


def isGitUrl(Url):
    """this function returns true, if the Url given as parameter is a git url:
    it either starts with git:// or the first part before the first '|' ends with .git
    or if the url starts with the token [git]"""
    if Url.startswith("git://"):
        return True
    # split away branch and tags
    splitUrl = Url.split("|")
    if splitUrl[0].endswith(".git"):
        return True
    if Url.startswith("[git]"):
        return True
    return False


def isSvnUrl(url):
    """this function returns true, if the Url given as parameter is a svn url"""
    if url.startswith("[svn]"):
        return True
    elif "svn:" in url:
        return True
    return False


def splitVCSUrl(Url):
    """this function splits up an url provided by Url into the server name, the path, a branch or tag;
    it will return a list with 3 strings according to the following scheme:
    git://servername:path.git|4.5branch|v4.5.1 will result in ['git://servername:path.git', '4.5branch', 'v4.5.1']
    This also works for all other dvcs"""
    splitUrl = Url.split("|")
    if len(splitUrl) < 3:
        c = [x for x in splitUrl]
        for dummy in range(3 - len(splitUrl)):
            c.append("")
    else:
        c = splitUrl[0:3]
    return c


def replaceVCSUrl(Url):
    """this function should be used to replace the url of a server
    this comes in useful if you e.g. need to switch the server url for a push url on gitorious.org"""
    configfile = os.path.join(CraftCore.standardDirs.etcBlueprintDir(), "..", "crafthosts.conf")
    replacedict = dict()

    # FIXME handle svn/git usernames and settings with a distinct naming
    # todo WTF
    if ("General", "KDESVNUSERNAME") in CraftCore.settings and CraftCore.settings.get("General", "KDESVNUSERNAME") != "username":
        replacedict["git://git.kde.org/"] = "git@git.kde.org:"
    if os.path.exists(configfile):
        config = configparser.ConfigParser()
        config.read(configfile)
        # add the default KDE stuff if the KDE username is set.
        for section in config.sections():
            host = config.get(section, "host")
            replace = config.get(section, "replace")
            replacedict[host] = replace

    for host in list(replacedict.keys()):
        if not Url.find(host) == -1:
            Url = Url.replace(host, replacedict[host])
            break
    return Url


def createImportLibs(dll_name, basepath):
    """creating the import libraries for the other compiler(if ANSI-C libs)"""

    dst = os.path.join(basepath, "lib")
    if not os.path.exists(dst):
        os.mkdir(dst)

    # check whether the required binary tools exist
    HAVE_GENDEF = CraftCore.cache.findApplication("gendef") is not None
    USE_GENDEF = HAVE_GENDEF
    HAVE_LIB = CraftCore.cache.findApplication("lib") is not None
    HAVE_DLLTOOL = CraftCore.cache.findApplication("dlltool") is not None

    CraftCore.log.debug(f"gendef found: {HAVE_GENDEF}")
    CraftCore.log.debug(f"gendef used: {USE_GENDEF}")
    CraftCore.log.debug(f"lib found: {HAVE_LIB}")
    CraftCore.log.debug(f"dlltool found: {HAVE_DLLTOOL}")

    dllpath = os.path.join(basepath, "bin", "%s.dll" % dll_name)
    defpath = os.path.join(basepath, "lib", "%s.def" % dll_name)
    exppath = os.path.join(basepath, "lib", "%s.exp" % dll_name)
    imppath = os.path.join(basepath, "lib", "%s.lib" % dll_name)
    gccpath = os.path.join(basepath, "lib", "%s.dll.a" % dll_name)

    if not HAVE_GENDEF and os.path.exists(defpath):
        HAVE_GENDEF = True
        USE_GENDEF = False
    if not HAVE_GENDEF:
        CraftCore.log.warning("system does not have gendef.exe")
        return False
    if not HAVE_LIB and not os.path.isfile(imppath):
        CraftCore.log.warning("system does not have lib.exe (from msvc)")
    if not HAVE_DLLTOOL and not os.path.isfile(gccpath):
        CraftCore.log.warning("system does not have dlltool.exe")

    # create .def
    if USE_GENDEF:
        cmd = "gendef - %s -a > %s " % (dllpath, defpath)
        system(cmd)

    if HAVE_LIB and not os.path.isfile(imppath):
        # create .lib
        cmd = "lib /machine:x86 /def:%s /out:%s" % (defpath, imppath)
        system(cmd)

    if HAVE_DLLTOOL and not os.path.isfile(gccpath):
        # create .dll.a
        cmd = "dlltool -d %s -l %s -k" % (defpath, gccpath)
        system(cmd)

    if os.path.exists(defpath):
        os.remove(defpath)
    if os.path.exists(exppath):
        os.remove(exppath)
    return True


def createSymlink(source, linkName, useAbsolutePath=False, targetIsDirectory=False):
    if not useAbsolutePath and os.path.isabs(linkName):
        srcPath = linkName
        srcPath = os.path.dirname(srcPath)
        source = os.path.relpath(source, srcPath)
    createDir(os.path.dirname(linkName))
    CraftCore.log.debug(f"creating symlink: {linkName} -> {source}")
    try:
        os.symlink(source, linkName, targetIsDirectory)
        return True
    except Exception as e:
        CraftCore.log.warning(e)
        return False


def createDir(path):
    """Recursive directory creation function. Makes all intermediate-level directories needed to contain the leaf directory"""
    if not os.path.lexists(path):
        CraftCore.log.debug(f"creating directory {path}")
        os.makedirs(path)
    return True


def copyFile(
    src: Path,
    dest: Path,
    linkOnly=CraftCore.settings.getboolean("General", "UseHardlinks", False),
):
    """copy file from src to dest"""
    CraftCore.log.debug("copy file from %s to %s" % (src, dest))
    src = Path(src)
    dest = Path(dest)
    if dest.is_dir():
        dest = dest / src.name
    else:
        createDir(dest.parent)
    if os.path.lexists(dest):
        CraftCore.log.warning(f"Overriding:\t{dest} with\n\t\t{src}")
        if src == dest:
            CraftCore.log.error(f"Can't copy a file into itself {src}=={dest}")
            return False
        OsUtils.rm(dest, True)
    # don't link to links
    if linkOnly and not os.path.islink(src):
        try:
            os.link(src, dest)
            return True
        except:
            CraftCore.log.warning(f"Failed to create hardlink {dest} for {src}")
    try:
        shutil.copy2(src, dest, follow_symlinks=False)
    except PermissionError as e:
        if CraftCore.compiler.isWindows and dest.exists():
            return deleteFile(dest) and copyFile(src, dest)
        else:
            raise e
    except Exception as e:
        CraftCore.log.error(f"Failed to copy file:\n{src} to\n{dest}", exc_info=e)
        return False
    return True


def copyDir(
    srcdir,
    destdir,
    linkOnly=CraftCore.settings.getboolean("General", "UseHardlinks", False),
    copiedFiles=None,
):
    """copy directory from srcdir to destdir"""
    CraftCore.log.debug("copyDir called. srcdir: %s, destdir: %s" % (srcdir, destdir))

    srcdir = Path(srcdir)
    if not srcdir.exists():
        CraftCore.log.warning(f"copyDir called. srcdir: {srcdir} does not exists")
        return False
    destdir = Path(destdir)
    if not destdir.exists():
        createDir(destdir)

    try:
        with os.scandir(srcdir) as scan:
            for entry in scan:
                dest = destdir / Path(entry.path).parent.relative_to(srcdir) / entry.name
                if entry.is_dir():
                    if entry.is_symlink():
                        # copy the symlinks without resolving them
                        if not copyFile(entry.path, dest, linkOnly=False):
                            return False
                        if copiedFiles is not None:
                            copiedFiles.append(str(dest))
                    else:
                        if not copyDir(entry.path, dest, copiedFiles=copiedFiles, linkOnly=linkOnly):
                            return False
                else:
                    # symlinks to files are included in `files`
                    if not copyFile(entry.path, dest, linkOnly=linkOnly):
                        return False
                    if copiedFiles is not None:
                        copiedFiles.append(str(dest))
    except Exception as e:
        CraftCore.log.error(f"Failed to copy dir:\n{srcdir} to\n{destdir}", exc_info=e)
        return False
    return True


def globCopyDir(
    srcDir: str,
    destDir: str,
    pattern: list[str],
    linkOnly=CraftCore.settings.getboolean("General", "UseHardlinks", False),
) -> bool:
    files = []
    for p in pattern:
        files.extend(glob.glob(os.path.join(srcDir, p), recursive=True))
    for f in files:
        if not copyFile(f, os.path.join(destDir, os.path.relpath(f, srcDir)), linkOnly=linkOnly):
            return False
    return True


def mergeTree(srcdir, destdir):
    """moves directory from @p srcdir to @p destdir

    If a directory in @p destdir exists, just write into it
    """
    srcdir = Path(srcdir)
    destdir = Path(destdir)
    if not createDir(destdir):
        return False

    CraftCore.log.debug(f"mergeTree called. srcdir: {srcdir}, destdir: {destdir}")
    if srcdir.samefile(destdir):
        CraftCore.log.critical(f"mergeTree called on the same directory srcdir: {srcdir}, destdir: {destdir}")
        return False

    with os.scandir(srcdir) as scan:
        for src in scan:
            dest = destdir / src.name
            if Path(src.path) in dest.parents:
                CraftCore.log.info(f"mergeTree: skipping moving of {src.path} to {dest}")
                continue
            if dest.exists():
                if dest.is_dir():
                    if dest.is_symlink():
                        if dest.samefile(src):
                            CraftCore.log.info(f"mergeTree: skipping moving of {src.path} to {dest} as a symlink with the same destination already exists")
                            continue
                        else:
                            CraftCore.log.critical(f"mergeTree failed: {src.path} and {dest} are both symlinks but point to different folders")
                            return False
                    if src.is_symlink() and not dest.is_symlink():
                        CraftCore.log.critical(f"mergeTree failed: how to merge symlink {src.path} into {dest}")
                        return False
                    if not src.is_symlink() and dest.is_symlink():
                        CraftCore.log.critical(f"mergeTree failed: how to merge folder {src.path} into symlink {dest}")
                        return False
                    if not mergeTree(src.path, dest):
                        return False
                else:
                    CraftCore.log.critical(
                        f"mergeTree failed: how to merge folder {src.path} into file {dest}\n"
                        f"If this error occured during packaging, consider extending the blacklist."
                    )
                    return False
            else:
                if not moveFile(src.path, destdir):
                    return False

    if not os.listdir(srcdir):
        # Cleanup (only removing empty folders)
        return rmtree(srcdir)
    else:
        # we move a directory in one of its sub directories
        assert srcdir in destdir.parents
        return True


@deprecated("moveFile")
def moveDir(srcdir, destdir):
    """move directory from srcdir to destdir"""
    return moveFile(srcdir, destdir)


def moveFile(src, dest):
    """move file from src to dest"""
    CraftCore.log.debug(f"move file from {src} to {dest}")
    try:
        shutil.move(
            src,
            dest,
            copy_function=lambda src, dest, *kw: shutil.copy2(src, dest, *kw, follow_symlinks=False),
        )
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True


def rmtree(directory):
    """recursively delete directory"""
    CraftCore.log.debug("rmtree called. directory: %s" % (directory))
    try:
        shutil.rmtree(directory, True)  # ignore errors
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True


def deleteFile(fileName):
    """delete file"""
    if not os.path.exists(fileName):
        return False
    return OsUtils.rm(fileName)


def putenv(name, value):
    """set environment variable"""
    if value is None:
        msg = f"unset environment variable -- unset {name}"
        if name in os.environ:
            del os.environ[name]
    else:
        msg = f"set environment variable -- set {name}={value}"
        os.environ[name] = value
    if CraftCore.settings.getboolean("CraftDebug", "PrintPutEnv", False):
        CraftCore.log.info(msg)
    else:
        CraftCore.log.debug(msg)
    return True


def applyPatch(sourceDir, f, patchLevel="0"):
    """apply single patch"""
    f = Path(f)
    if f.is_dir():
        # apply a whole dir of patches
        out = True
        with os.scandir(f) as scan:
            for patch in scan:
                if patch.is_file() and not patch.name.startswith("."):
                    out = applyPatch(sourceDir, f / patch, patchLevel) and out
        return out
    with Dos2UnixFile(f) as unixFile:
        cmd = ["patch", "--ignore-whitespace", "-d", Path(sourceDir).as_posix(), "-p", str(patchLevel), "-i", unixFile]
        result = system(cmd)
    if not result:
        CraftCore.log.warning(f"applying {f} failed!")
    return result


def embedManifest(executable, manifest):
    """
    Embed a manifest to an executable using either the free
    kdewin manifest if it exists in dev-utils/bin
    or the one provided by the Microsoft Platform SDK if it
    is installed'
    """
    if not os.path.isfile(executable) or not os.path.isfile(manifest):
        # We die here because this is a problem with the blueprint files
        CraftCore.log.critical("embedManifest %s or %s do not exist" % (executable, manifest))
    CraftCore.log.debug("embedding ressource manifest %s into %s" % (manifest, executable))
    return system(["mt", "-nologo", "-manifest", manifest, f"-outputresource:{executable};1"])


def notify(title, message, alertClass=None, log=True):
    if log:
        CraftCore.debug.step(f"{title}: {message}")
    default = ""
    if CraftCore.compiler.isMacOS:
        default = "TerminalNotifier"
    backends = CraftCore.settings.getList("General", "Notify", default)

    if backends == ["None"]:
        return
    if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) or backends == "":
        return
    backends = Notifier.NotificationLoader.load(backends)
    for backend in backends.values():
        backend.notify(title, message, alertClass)


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# kw is forwareded to system
# keepArgv0 controls whether the kshimgen will be called with the --keep-argv0 flag to emulate symlinks
def createShim(shim, target, args=None, guiApp=False, useAbsolutePath=False, keepArgv0=False, env=None, **kw) -> bool:
    if not useAbsolutePath and os.path.isabs(target):
        target = os.path.relpath(target, os.path.dirname(shim))
    createDir(os.path.dirname(shim))

    if os.path.exists(shim):
        deleteFile(shim)
    if not args:
        args = []
    elif isinstance(args, str):
        CraftCore.log.error("Please pass args as list[str]")
        return system(f"kshimgen --create {shim} {target} -- {args}")
    command = ["kshimgen", "--create", shim, target]
    if CraftCore.compiler.isWindows and guiApp:
        command.append("--gui")
    if keepArgv0:
        command.append("--keep-argv0")
    if env:
        for k, v in env.items():
            command += ["--env", f"{k}={v}"]
    return system(command + ["--"] + args, **kw)


def replaceSymlinksWithCopies(path, _replaceDirs=False):
    assert CraftCore.compiler.isWindows

    def resolveLink(path):
        while os.path.islink(path):
            toReplace = os.readlink(path)
            if not os.path.isabs(toReplace):
                path = os.path.join(os.path.dirname(path), toReplace)
            else:
                path = toReplace
        return path

    # symlinks to dirs are resolved after we resolved the files
    dirsToResolve = []
    ok = True
    for root, _, files in os.walk(path):
        for svg in files:
            if not ok:
                return False
            path = os.path.join(root, svg)
            if os.path.islink(path):
                toReplace = resolveLink(path)
                if not os.path.exists(toReplace):
                    CraftCore.log.error(f"Resolving {path} failed: {toReplace} does not exists.")
                    continue
                if toReplace != path:
                    if os.path.isdir(toReplace):
                        if not _replaceDirs:
                            dirsToResolve.append(path)
                        else:
                            os.unlink(path)
                            ok = copyDir(toReplace, path)
                    else:
                        os.unlink(path)
                        ok = copyFile(toReplace, path)
    while dirsToResolve:
        d = dirsToResolve.pop()
        if not os.path.exists(resolveLink(d)):
            CraftCore.log.warning(f"Delay replacement of {d}")
            dirsToResolve.append(d)
            continue
        if not replaceSymlinksWithCopies(os.path.dirname(d), _replaceDirs=True):
            return False
    return True


class ProgressBar(object):
    def __init__(self, initialProgess=0):
        self._lastValue = None
        self._initialProgress = initialProgess
        # don't try experiemtns on old terminals
        self._legacyMode = not CraftCore.settings.getboolean("General", "AllowAnsiColor")

    def print(self, progress: int, force: bool = False):
        progress = int(progress)
        progress = max(0, progress)
        progress = min(100, progress)
        if not force and not os.isatty(sys.stderr.fileno()):
            return
        if self._lastValue == progress:
            return
        self._lastValue = progress
        width, _ = shutil.get_terminal_size((80, 20))
        if self._legacyMode:
            width -= 20  # margin
            times = int(width / 100 * progress)
            sys.stderr.write("\r{percent}% [{progress}{space}]".format(progress="#" * times, space=" " * (width - times), percent=progress))
        else:
            width -= 5  # margin
            times = int(width / 100 * progress)
            sys.stderr.write(
                "\r{percent}% {progress}{fill}".format(
                    progress="\u2588" * times,
                    fill="\u2591" * (width - times),
                    percent=progress,
                )
            )
        sys.stderr.flush()

    def __enter__(self):
        self.print(self._initialProgress, True)
        return self

    def __exit__(self, exc_type, exc_value, trback):
        self.print(100, True)
        CraftCore.debug.new_line()


class ScopedEnv(object):
    def __init__(self, env):
        self.oldEnv = {}
        for key, value in env.items():
            self.oldEnv[key] = os.environ.get(key, None)
            putenv(key, str(value) if value is not None else None)

    def reset(self):
        for key, value in self.oldEnv.items():
            putenv(key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        self.reset()


def configureFile(inFile: str, outFile: str, variables: dict) -> bool:
    CraftCore.log.debug(f"configureFile {inFile} -> {outFile}\n{variables}")
    configPatter = re.compile(r"@{([^{}]+)}")
    with open(inFile, "rt", encoding="UTF-8") as f:
        script = f.read()
    matches = configPatter.findall(script)
    if not matches:
        CraftCore.log.debug("Nothing to configure")
        return False

    while matches:
        for match in matches:
            val = variables.get(match, None)
            if val is None:
                linenUmber = 0
                for line in script.split("\n"):
                    if match in line:
                        break
                    linenUmber += 1
                raise Exception(f"Failed to configure {inFile}: @{{{match}}} is not in variables\n" f"{linenUmber}:{line}")
            script = script.replace(f"@{{{match}}}", str(val))
        matches = configPatter.findall(script)

    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    with open(outFile, "wt", encoding="UTF-8") as f:
        f.write(script)
    return True


def limitCommandLineLength(command: list[str], args: list[str]) -> list[list[str]]:
    if CraftCore.compiler.isWindows:
        # https://docs.microsoft.com/en-US/troubleshoot/windows-client/shell-experience/command-line-string-limitation
        SIZE = 8191
    else:
        code, result = CraftCore.cache.getCommandOutput("getconf", "ARG_MAX")
        if code != 0:
            return False
        SIZE = int(result.strip())
    out = []
    commandSize = sum(map(lambda c: len(str(c)), command))
    if commandSize >= SIZE:
        CraftCore.log.error("Failed to compute command, command too long")
        return []
    currentSize = commandSize
    tmp = []
    for a in args:
        a = str(a)
        le = len(a)
        if currentSize + le >= SIZE:
            out.append(command + tmp)
            tmp = []
            currentSize = commandSize
        tmp.append(a)
        currentSize += le
    if tmp:
        out.append(command + tmp)
    return out


# includeShellScripts, on windows this will also check for shell scripts
def isExecuatable(fileName: Path, includeShellScripts=False):
    fileName = Path(fileName)
    if CraftCore.compiler.isWindows:
        if fileName.suffix.upper() in os.environ["PATHEXT"].split(";"):
            return True
        if includeShellScripts:
            signature = b"#!"
            with fileName.open("rb") as f:
                return f.read(len(signature)) == signature
    else:
        return os.access(fileName, os.X_OK)
    return False


def isBinary(fileName: str) -> bool:
    # https://en.wikipedia.org/wiki/List_of_file_signatures
    MACH_O_64 = b"\xCF\xFA\xED\xFE"
    ELF = b"\x7F\x45\x4C\x46"

    fileName = Path(fileName)
    suffix = fileName.suffix.lower()
    if fileName.is_symlink() or fileName.is_dir():
        return False
    if CraftCore.compiler.isWindows:
        if suffix in {".dll", ".exe"}:
            return True
    else:
        if CraftCore.compiler.isMacOS:
            if ".dSYM/" in str(fileName):
                return False
        elif suffix == ".debug":
            return False
        if suffix in {".so", ".dylib"}:
            return True
        else:
            if CraftCore.compiler.isMacOS:
                signature = MACH_O_64
            elif CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD or CraftCore.compiler.isAndroid:
                signature = ELF
            else:
                raise Exception("Unsupported platform")
            with fileName.open("rb") as f:
                return f.read(len(signature)) == signature
    return False


def isScript(fileName: str):
    fileName = Path(fileName)
    if fileName.is_symlink() or fileName.is_dir():
        return False
    if isExecuatable(fileName):
        if CraftCore.compiler.isWindows and not fileName.suffix.lower() == ".exe":
            return True
        signature = b"#!"
        with fileName.open("rb") as f:
            return f.read(len(signature)) == signature
    return False


def getLibraryDeps(path):
    deps = []
    if CraftCore.compiler.isMacOS:
        # based on https://github.com/qt/qttools/blob/5.11/src/macdeployqt/shared/shared.cpp
        infoRe = re.compile("^\\t(.+) \\(compatibility version (\\d+\\.\\d+\\.\\d+), " + "current version (\\d+\\.\\d+\\.\\d+)\\)$")
        with io.StringIO() as log:
            if not system(["otool", "-L", path], stdout=log, logCommand=False):
                return []
            lines = log.getvalue().strip().split("\n")
        lines.pop(0)  # name of the library
        for line in lines:
            match = infoRe.match(line)
            if match:
                deps.append(match[1])
    return deps


def getRpath(path: Path):
    patchElf = CraftCore.standardDirs.craftRoot() / "dev-utils/bin/patchelf"
    with io.StringIO() as log:
        if not system([patchElf, "--print-rpath", path], stdout=log, stderr=subprocess.STDOUT, logCommand=False):
            if str(path).endswith(".cpp.o"):
                CraftCore.log.info("Ignoring rpath error on .o file. This is a workaround for Qt installing garbage.")
                return {}
            elif "The input file is most likely statically linked" in log.getvalue():
                CraftCore.log.info("Ignoring rpath error on statically linked file.")
                return {}
            else:
                return None
        return set(filter(None, log.getvalue().strip().split(":")))


def updateRpath(path: Path, oldRpath: set, newRpath: set):
    patchElf = CraftCore.standardDirs.craftRoot() / "dev-utils/bin/patchelf"
    if newRpath != oldRpath:
        CraftCore.log.debug(f"Updating rpath for {path}: {oldRpath} -> {newRpath}")
        if not system([patchElf, "--set-rpath", ":".join(newRpath), path], logCommand=False):
            return False
    return True


def regexFileFilter(filename: os.DirEntry, root: str, patterns: list[re.Pattern] = None) -> bool:
    """return False if file does not match pattern"""
    # use linux style seperators
    relFilePath = Path(filename.path).relative_to(root).as_posix()
    for pattern in patterns:
        if pattern.search(relFilePath):
            CraftCore.log.debug(f"regExDirFilter: {relFilePath} matches: {pattern.pattern}")
            return True
    return False


def filterDirectoryContent(
    root,
    whitelist=lambda f, root: True,
    blacklist=lambda g, root: False,
    allowBadSymlinks=False,
    handleAppBundleAsFile=False,
):
    """
    Traverse through a directory tree and return every
    filename that the function whitelist returns as true and
    which do not match blacklist entries
    """
    if not os.path.exists(root):
        return
    dirs = [root]
    while dirs:
        path = dirs.pop()
        with os.scandir(path) as scan:
            for filePath in scan:
                if not allowBadSymlinks and filePath.is_symlink():
                    if Path(root).resolve() not in Path(filePath.path).resolve().parents:
                        CraftCore.log.debug(f"filterDirectoryContent: skipping {filePath.path}, it is not located under {root}")
                        continue
                if filePath.is_dir(follow_symlinks=False):
                    # handle .app folders and dsym as files
                    if CraftCore.compiler.isMacOS:
                        suffixes = {".dsym"}
                        if handleAppBundleAsFile:
                            suffixes.update({".app", ".framework"})
                        if Path(filePath.path).suffix.lower() not in suffixes:
                            dirs.append(filePath.path)
                            continue
                    else:
                        dirs.append(filePath.path)
                        continue
                if blacklist(filePath, root=root) and not whitelist(filePath, root=root):
                    continue
                elif filePath.is_dir():
                    yield filePath.path
                elif filePath.is_file():
                    yield filePath.path
                elif filePath.is_symlink():
                    if not allowBadSymlinks:
                        CraftCore.log.warning(f"{filePath.path} is an invalid link ({os.readlink(filePath.path)})")
                        continue
                    else:
                        yield filePath.path
                else:
                    CraftCore.log.warning(f"Unhandled case: {filePath}")
                    raise Exception(f"Unhandled case: {filePath}")


def makeWritable(targetPath: Path, log: bool = True) -> list[bool, int]:
    """Make a file writable if needed. Returns if the mode was changed and the curent mode of the file"""
    targetPath = Path(targetPath)
    originalMode = targetPath.stat().st_mode
    if not bool(originalMode & stat.S_IWUSR):
        newMode = originalMode | stat.S_IWUSR
        targetPath.chmod(newMode)
        if log:
            CraftCore.log.info(f"Made {targetPath} writeable")
        return (True, newMode)
    return (False, originalMode)


@contextlib.contextmanager
def makeTemporaryWritable(targetPath: Path):
    targetPath = Path(targetPath)
    wasReadOnly = False
    mode = 0
    try:
        # ensure it is writable
        wasReadOnly, mode = makeWritable(targetPath, log=False)
        yield targetPath
    finally:
        if wasReadOnly:
            targetPath.chmod(mode & ~stat.S_IWUSR)


def getPDBForBinary(path: str) -> Path:
    with open(path, "rb") as f:
        data = f.read()
    pdb = data.rfind(b".pdb")
    if pdb != -1:
        return Path(data[(data.rfind(0x00, 0, pdb) + 1) : pdb + 4].decode("utf-8"))
    return None


def installShortcut(name: str, path: str, workingDir: str, icon: str, desciption: str):
    if not CraftCore.compiler.isWindows:
        return True
    from shells import Powershell

    pwsh = Powershell()
    shortcutPath = Path(os.environ["APPDATA"]) / f"Microsoft/Windows/Start Menu/Programs/Craft/{name}.lnk"
    shortcutPath.parent.mkdir(parents=True, exist_ok=True)

    return pwsh.execute(
        [
            os.path.join(CraftCore.standardDirs.craftBin(), "install-lnk.ps1"),
            "-Path",
            pwsh.quote(path),
            "-WorkingDirectory",
            pwsh.quote(OsUtils.toNativePath(workingDir)),
            "-Name",
            pwsh.quote(shortcutPath),
            "-Icon",
            pwsh.quote(icon),
            "-Description",
            pwsh.quote(desciption),
        ]
    )


def symFileName(fileName: Path) -> Path:
    if CraftCore.compiler.isMacOS:
        bundleDir = list(
            filter(
                lambda x: x.name.endswith(".framework") or x.name.endswith(".app"),
                fileName.parents,
            )
        )
        if bundleDir:
            suffix = ""
            # if we are a .app in a .framework we put the smbols in the same location
            if len(bundleDir) > 1:
                suffix = f"-{'.'.join([x.name for x in reversed(bundleDir[0:-1])])}"
            return Path(f"{bundleDir[-1]}{suffix}{CraftCore.compiler.symbolsSuffix}") / "Contents/Resources/DWARF" / fileName.name
        else:
            return Path(f"{fileName}{CraftCore.compiler.symbolsSuffix}")
    else:
        return Path(f"{fileName}{CraftCore.compiler.symbolsSuffix}")


def strip(fileName: Path, destFileName: Optional[Path] = None) -> Path:
    """strip debugging informations from shared libraries and executables"""
    """ Returns the path to the sym file on success, None on error"""
    if CraftCore.compiler.isMSVC() or not CraftCore.compiler.isGCCLike():
        raise Exception(f"Skipping stripping of {fileName} -- either disabled or unsupported with this compiler")

    fileName = Path(fileName)
    if not destFileName:
        destFileName = symFileName(fileName)
    if destFileName.exists():
        return destFileName

    if CraftCore.compiler.isMacOS:
        if not (system(["/usr/bin/dsymutil", fileName, "-o", destFileName]) and system(["strip", "-x", "-S", fileName]) and localSignMac([fileName])):
            return None
    else:
        if CraftCore.compiler.isAndroid:
            toolchain_path = os.path.join(os.environ["ANDROID_NDK"], "toolchains/llvm/prebuilt", os.environ.get("ANDROID_NDK_HOST", "linux-x86_64"), "bin")
            objcopy = os.path.join(toolchain_path, "llvm-objcopy")
            strip = os.path.join(toolchain_path, "llvm-strip")
        else:
            objcopy = "objcopy"
            strip = "strip"
        if not (
            system([objcopy, "--only-keep-debug", fileName, destFileName])
            and system([strip, "--strip-debug", "--strip-unneeded", fileName])
            and system([objcopy, "--add-gnu-debuglink", destFileName, fileName])
        ):
            return None
    return destFileName


def urljoin(root, path):
    return "/".join([root.rstrip("/"), path])


def redact(input: str, secrests: set[str]):
    if secrests is None:
        return input
    if isinstance(input, str):
        for s in secrests:
            input = input.replace(s, "***")
        return input
    elif isinstance(input, list):
        out = []
        for var in input:
            for s in secrests:
                out.append(var.replace(s, "***"))
        return out


def localSignMac(binaries):
    # TODO: this rather fits to CodeSign.py but we would end up with circular import in utils.strip
    CraftCore.log.debug(f"Local signing {[str(x) for x in binaries]}")
    signCommand = ["codesign", "-s", "-", "-f", "--deep", "--preserve-metadata=identifier,entitlements", "--verbose=99"]
    for command in limitCommandLineLength(signCommand, binaries):
        with StageLogger("localSignMac", buffered=True, outputOnFailure=True):
            if not system(command, logCommand=False):
                return False
    return True
