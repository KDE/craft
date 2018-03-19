# -*- coding: utf-8 -*-
"""@brief utilities
this file contains some helper functions for craft
"""

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Ralf Habacker <ralf.habacker [AT] freenet [DOT] de>

import inspect
import io
import os
import re
import shlex
import subprocess
import urllib.error
import urllib.parse
import urllib.request

import Notifier.NotificationLoader
from CraftConfig import *
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from CraftStandardDirs import CraftStandardDirs
import Utils.CraftCache
from CraftDebug import deprecated

def abstract():
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

### fetch functions

def getFiles(urls, destdir, suffix='', filenames=''):
    """download files from 'url' into 'destdir'"""
    CraftCore.log.debug("getfiles called. urls: %s, filenames: %s, suffix: %s" % (urls, filenames, suffix))
    # make sure distfiles dir exists
    if (not os.path.exists(destdir)):
        os.makedirs(destdir)

    if type(urls) == list:
        urlList = urls
    else:
        urlList = urls.split()

    if filenames == '':
        filenames = [os.path.basename(x) for x in urlList]

    if type(filenames) == list:
        filenameList = filenames
    else:
        filenameList = filenames.split()

    dlist = list(zip(urlList, filenameList))

    for url, filename in dlist:
        if (not getFile(url + suffix, destdir, filename)):
            return False

    return True


def getFile(url, destdir, filename='') -> bool:
    """download file from 'url' into 'destdir'"""
    CraftCore.log.debug("getFile called. url: %s" % url)
    if url == "":
        CraftCore.log.error("fetch: no url given")
        return False

    if not filename:
        _, _, path, _, _, _ = urllib.parse.urlparse(url)
        filename = os.path.basename(path)

    if CraftCore.cache.findApplication("curl"):
        return curlFile(url, destdir, filename)

    if CraftCore.cache.findApplication("wget"):
        return wgetFile(url, destdir, filename)

    if os.path.exists(os.path.join(destdir, filename)):
        return True

    if CraftCore.cache.findApplication("powershell"):
        powershell = CraftCore.cache.findApplication("powershell")
        filename = os.path.join(destdir, filename)
        return system([powershell, "-NoProfile", "-Command",
                       f"(new-object net.webclient).DownloadFile('{url}', '{filename}')"])
    else:
        def dlProgress(count, blockSize, totalSize):
            if totalSize != -1:
                percent = int(count * blockSize * 100 / totalSize)
                printProgress(percent)
            else:
                sys.stdout.write(("\r%s bytes downloaded" % (count * blockSize)))
                sys.stdout.flush()

        try:
            urllib.request.urlretrieve(url, filename=os.path.join(destdir, filename),
                                       reporthook=dlProgress if CraftCore.debug.verbose() >= 0 else None)
        except Exception as e:
            CraftCore.log.warning(e)
            return False

    if CraftCore.debug.verbose() >= 0:
        sys.stdout.write("\n")
        sys.stdout.flush()
    return True


def curlFile(url, destdir, filename=''):
    """download file with curl from 'url' into 'destdir', if filename is given to the file specified"""
    curl = CraftCore.cache.findApplication("curl")
    command = [curl, "-C", "-", "--retry", "10", "-L", "--ftp-ssl"]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--cacert", cert]
    # the default of 20 might not be enough for sourceforge ...
    command += ["--max-redirs",  "50"]
    if not filename:
        # Curl can't download to a custom directory on its own
        return False
    else:
        command += ["-o", os.path.join(destdir, filename)]
    command += [url]
    CraftCore.log.debug("curlfile called")

    if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) and CraftCore.debug.verbose() < 1 and CraftCore.cache.checkCommandOutputFor(curl, "--progress-bar"):
        command += ["--progress-bar"]
        CraftCore.log.info(f"curl {url}")
        return system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    else:
        if CraftCore.debug.verbose() > 0:
            command += ["-v"]
        return system(command)


def wgetFile(url, destdir, filename=''):
    """download file with wget from 'url' into 'destdir', if filename is given to the file specified"""
    wget = CraftCore.cache.findApplication("wget")
    command = [wget, "-c", "-t", "10"]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--ca-certificate", cert]
    # the default of 20 might not be enough for sourceforge ...
    command += ["--max-redirect",  "50"]
    if CraftCore.settings.getboolean("General", "EMERGE_NO_PASSIVE_FTP", False):
        command += ["--no-passive-ftp"]
    if not filename:
        command += ["-P", destdir]
    else:
        command += ["-O", os.path.join(destdir, filename)]
    command += [url]
    CraftCore.log.debug("wgetfile called")

    if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) and CraftCore.debug.verbose() < 1 and CraftCore.cache.checkCommandOutputFor(wget, "--show-progress"):
        command += ["-q", "--show-progress"]
        CraftCore.log.info(f"wget {url}")
        return system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    else:
        return system(command)


### unpack functions

def unpackFiles(downloaddir, filenames, workdir):
    """unpack (multiple) files specified by 'filenames' from 'downloaddir' into 'workdir'"""

    for filename in filenames:
        if (not unpackFile(downloaddir, filename, workdir)):
            return False

    return True


def unpackFile(downloaddir, filename, workdir):
    """unpack file specified by 'filename' from 'downloaddir' into 'workdir'"""
    CraftCore.log.debug(f"unpacking this file: {filename}")
    if not filename:
        return True

    (shortname, ext) = os.path.splitext(filename)
    if ext == "":
        CraftCore.log.warning(f"unpackFile called on invalid file extension {filename}")
        return True
    elif OsUtils.isWin() and CraftCore.cache.findApplication("7za") and (
                OsUtils.supportsSymlinks() or not re.match("(.*\.tar.*$|.*\.tgz$)", filename)):
        return un7zip(os.path.join(downloaddir, filename), workdir, ext)
    elif ext == ".7z":
        return un7zip(os.path.join(downloaddir, filename), workdir, ext)
    else:
        try:
            shutil.unpack_archive(os.path.join(downloaddir, filename), workdir)
        except Exception as e:
            CraftCore.log.error(f"Failed to unpack {filename}", exc_info=e)
            return False
    return True


def un7zip(fileName, destdir, flag=None):
    kw = {}
    progressFlags = []
    type = []
    resolveSymlinks = False
    app = CraftCore.cache.findApplication("7za")
    if CraftCore.cache.checkCommandOutputFor(app, "-bs"):
        progressFlags = ["-bso2",  "-bsp1"]
        kw["stderr"] = subprocess.PIPE

    if flag == ".7z":
        # Actually this is not needed for a normal archive.
        # But git is an exe file renamed to 7z and we need to specify the type.
        # Yes it is an ugly hack.
        type = ["-t7z"]
    if re.match("(.*\.tar.*$|.*\.tgz$)", fileName):
        type = ["-ttar"]
        kw["pipeProcess"] = subprocess.Popen([app, "x", fileName, "-so"], stdout = subprocess.PIPE)
        if OsUtils.isWin():
            resolveSymlinks = True
            command = [app, "x", "-si", f"-o{destdir}"]+ type + progressFlags
        else:
            tar = CraftCore.cache.findApplication("tar")
            command = [tar, "--directory", destdir, "-xvf", "-"]
            kw = {}
    else:
        command = [app, "x", "-r", "-y", f"-o{destdir}", fileName] + type + progressFlags

    # While 7zip supports symlinks cmake 3.8.0 does not support symlinks
    return system(command, displayProgress=True, **kw) and not resolveSymlinks or replaceSymlinksWithCopys(destdir)


def system(cmd, displayProgress=False, logCommand=True, acceptableExitCodes=None, **kw):
    """execute cmd in a shell. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options."""
    return systemWithoutShell(cmd, displayProgress=displayProgress, logCommand=logCommand, acceptableExitCodes=acceptableExitCodes, **kw)


def systemWithoutShell(cmd, displayProgress=False, logCommand=True, pipeProcess=None, acceptableExitCodes=None, **kw):
    """execute cmd. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options.

    When the parameter "displayProgress" is True, stdout won't be
    logged to allow the display of progress bars."""

    environment = kw.get("env", os.environ)
    cwd = kw.get("cwd", os.getcwd())

    # if the first argument is not an absolute path replace it with the full path to the application
    if isinstance(cmd, list):
        arg0 = cmd[0]
        if not "shell" in kw:
            kw["shell"] = False
    else:
        if not "shell" in kw:
            # use shell, arg0 might end up with "/usr/bin/svn" => needs shell so it can be executed
            kw["shell"] = True
        arg0 = shlex.split(cmd, posix=False)[0]

    matchQuoted = re.match("^\"(.*)\"$", arg0)
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
            cmd = cmd.replace(arg0, f"\"{app}\"", 1)
    else:
        app = arg0

    if logCommand:
        _logCommand = ""
        if pipeProcess:
            _logCommand = "{0} | ".format(" ".join(pipeProcess.args))
        _logCommand += " ".join(cmd) if isinstance(cmd, list) else cmd
        CraftCore.debug.print("executing command: {0}".format(_logCommand))
    if pipeProcess:
        CraftCore.log.debug(f"executing command: {pipeProcess.args!r} | {cmd!r}")
    else:
        CraftCore.log.debug(f"executing command: {cmd!r}")
    CraftCore.log.debug(f"CWD: {cwd!r}")
    CraftCore.log.debug(f"displayProgress={displayProgress}")
    CraftCore.debug.logEnv(environment)
    if pipeProcess:
        kw["stdin"] = pipeProcess.stdout
    if not displayProgress or CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
        stdout = kw.get('stdout', sys.stdout)
        kw['stderr'] = subprocess.STDOUT
        kw['stdout'] = subprocess.PIPE
        proc = subprocess.Popen(cmd, **kw)
        if pipeProcess:
            pipeProcess.stdout.close()
        for line in proc.stdout:
            if isinstance(stdout, io.TextIOWrapper):
                if CraftCore.debug.verbose() < 3:  # don't print if we write the debug log to stdout anyhow
                    stdout.buffer.write(line)
                    stdout.flush()
            elif stdout == subprocess.DEVNULL:
                pass
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

    if acceptableExitCodes is None:
        ok = proc.returncode == 0
    else:
        ok = proc.returncode in acceptableExitCodes
    if not ok:
        CraftCore.log.debug(f"Command {cmd} failed with exit code {proc.returncode}")
    return ok

def cleanDirectory(directory):
    CraftCore.log.debug("clean directory %s" % directory)
    if (os.path.exists(directory)):
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if not OsUtils.rm(os.path.join(root, name), True):
                    CraftCore.log.critical("couldn't delete file %s\n ( %s )" % (name, os.path.join(root, name)))
            for name in dirs:
                if not OsUtils.rmDir(os.path.join(root, name), True):
                    CraftCore.log.critical("couldn't delete directory %s\n( %s )" % (name, os.path.join(root, name)))
    else:
        os.makedirs(directory)


def getVCSType(url):
    """ return the type of the vcs url """
    if not url:
        return ""
    if isGitUrl(url):
        return "git"
    elif isSvnUrl(url):
        return "svn"
    elif url.startswith("[hg]"):
        return "hg"
    ## \todo complete more cvs access schemes
    elif url.find("pserver:") >= 0:
        return "cvs"
    else:
        return ""


def isGitUrl(Url):
    """ this function returns true, if the Url given as parameter is a git url:
        it either starts with git:// or the first part before the first '|' ends with .git
        or if the url starts with the token [git] """
    if Url.startswith('git://'):
        return True
    # split away branch and tags
    splitUrl = Url.split('|')
    if splitUrl[0].endswith(".git"):
        return True
    if Url.startswith("[git]"):
        return True
    return False

def isSvnUrl(url):
    """ this function returns true, if the Url given as parameter is a svn url """
    if url.startswith("[svn]"):
        return True
    elif url.find("://") == -1:
        return True
    elif url.find("svn:") >= 0 or url.find("https:") >= 0 or url.find("http:") >= 0:
        return True
    return False

def splitVCSUrl(Url):
    """ this function splits up an url provided by Url into the server name, the path, a branch or tag;
        it will return a list with 3 strings according to the following scheme:
        git://servername/path.git|4.5branch|v4.5.1 will result in ['git://servername:path.git', '4.5branch', 'v4.5.1']
        This also works for all other dvcs"""
    splitUrl = Url.split('|')
    if len(splitUrl) < 3:
        c = [x for x in splitUrl]
        for dummy in range(3 - len(splitUrl)):
            c.append('')
    else:
        c = splitUrl[0:3]
    return c


def replaceVCSUrl(Url):
    """ this function should be used to replace the url of a server
        this comes in useful if you e.g. need to switch the server url for a push url on gitorious.org """
    configfile = os.path.join(CraftStandardDirs.etcBlueprintDir(), "..", "crafthosts.conf")
    replacedict = dict()

    # FIXME handle svn/git usernames and settings with a distinct naming
    # todo WTF
    if (("General", "KDESVNUSERNAME") in CraftCore.settings and
                CraftCore.settings.get("General", "KDESVNUSERNAME") != "username"):
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
    if (not os.path.exists(dst)):
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

    if (HAVE_LIB and not os.path.isfile(imppath)):
        # create .lib
        cmd = "lib /machine:x86 /def:%s /out:%s" % (defpath, imppath)
        system(cmd)

    if (HAVE_DLLTOOL and not os.path.isfile(gccpath)):
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
    if not os.path.exists(os.path.dirname(linkName)):
        os.makedirs(os.path.dirname(linkName))
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


def copyFile(src, dest, linkOnly=CraftCore.settings.getboolean("General", "UseHardlinks", False)):
    """ copy file from src to dest"""
    CraftCore.log.debug("copy file from %s to %s" % (src, dest))
    destDir = os.path.dirname(dest)
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    if os.path.lexists(dest):
        CraftCore.log.warning("Overriding %s" % dest)
        if not os.path.islink(dest) and os.path.samefile(src, dest):
            CraftCore.log.error(f"Can't copy a file into itself {src}=={dest}")
            return False
        OsUtils.rm(dest, True)
    # don't link to links
    if linkOnly and not os.path.islink(src):
        try:
            os.link(src, dest)
            return True
        except:
            CraftCore.log.warning("Failed to create hardlink %s for %s" % (dest, src))
    shutil.copy(src, dest, follow_symlinks=False)
    return True


def copyDir(srcdir, destdir, linkOnly=CraftCore.settings.getboolean("General", "UseHardlinks", False), copiedFiles=None):
    """ copy directory from srcdir to destdir """
    CraftCore.log.debug("copyDir called. srcdir: %s, destdir: %s" % (srcdir, destdir))

    if (not srcdir.endswith(os.path.sep)):
        srcdir += os.path.sep
    if (not destdir.endswith(os.path.sep)):
        destdir += os.path.sep

    try:
        for root, dirNames, files in os.walk(srcdir):
            tmpdir = root.replace(srcdir, destdir)
            for dirName in dirNames:
                if os.path.islink(os.path.join(root, dirName)):
                    # copy the symlinks without resolving them
                    if not copyFile(os.path.join(root, dirName), os.path.join(tmpdir, dirName), linkOnly=False):
                        return False
                    if copiedFiles is not None:
                        copiedFiles.append(os.path.join(tmpdir, dirName))
                else:
                    if not createDir(os.path.join(tmpdir, dirName)):
                        return False

            for fileName in files:
                # symlinks to files are included in `files`
                if not copyFile(os.path.join(root, fileName), os.path.join(tmpdir, fileName),linkOnly=linkOnly):
                    return False
                if copiedFiles is not None:
                    copiedFiles.append(os.path.join(tmpdir, fileName))
    except Exception as e:
        CraftCore.log.error(e)
        return False
    return True


def mergeTree(srcdir, destdir):
    """ moves directory from @p srcdir to @p destdir

    If a directory in @p destdir exists, just write into it
    """

    try:
        os.makedirs(destdir, exist_ok=True)
    except Exception as e:
        CraftCore.log.warning(e)
        return False

    CraftCore.log.debug(f"mergeTree called. srcdir: {srcdir}, destdir: {destdir}")
    if os.path.samefile(srcdir, destdir):
        CraftCore.log.critical(f"mergeTree called on the same directory srcdir: {srcdir}, destdir: {destdir}")
        return False

    fileList = os.listdir(srcdir)
    for i in fileList:
        src = os.path.join(srcdir, i)
        dest = os.path.join(destdir, i)
        if os.path.exists(dest):
            if os.path.isdir(dest):
                if not mergeTree(src, dest):
                    return False
                continue
            else:
                if not rmtree(dest):
                    return False
        if not moveDir(src, destdir):
            return False

    # Cleanup (only removing empty folders)
    return rmtree(srcdir)


def moveDir(srcdir, destdir):
    """ move directory from srcdir to destdir """
    CraftCore.log.debug("moveDir called. srcdir: %s, destdir: %s" % (srcdir, destdir))
    try:
        shutil.move(srcdir, destdir)
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True


def rmtree(directory):
    """ recursively delete directory """
    CraftCore.log.debug("rmtree called. directory: %s" % (directory))
    try:
        shutil.rmtree(directory, True)  # ignore errors
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True


def moveFile(src, dest):
    """move file from src to dest"""
    CraftCore.log.debug("move file from %s to %s" % (src, dest))
    try:
        shutil.move(src, dest)
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True


def deleteFile(fileName):
    """delete file """
    if not os.path.exists(fileName):
        return False
    CraftCore.log.debug("delete file %s " % (fileName))
    try:
        os.remove(fileName)
    except Exception as e:
        CraftCore.log.warning(e)
        return False
    return True

def putenv(name, value):
    """set environment variable"""
    CraftCore.log.debug("set environment variable -- set %s=%s" % (name, value))
    if not value:
        if name in os.environ:
            del os.environ[name]
    else:
        os.environ[name] = value
    return True


def applyPatch(sourceDir, f, patchLevel='0'):
    """apply single patch"""
    cmd = ["patch", "--ignore-whitespace", "-d", sourceDir, "-p", str(patchLevel), "-i", f]
    result = system(cmd)
    if not result:
        CraftCore.log.warning("applying %s failed!" % f)
    return result

def embedManifest(executable, manifest):
    '''
       Embed a manifest to an executable using either the free
       kdewin manifest if it exists in dev-utils/bin
       or the one provided by the Microsoft Platform SDK if it
       is installed'
    '''
    if not os.path.isfile(executable) or not os.path.isfile(manifest):
        # We die here because this is a problem with the blueprint files
        CraftCore.log.critical("embedManifest %s or %s do not exist" % (executable, manifest))
    CraftCore.log.debug("embedding ressource manifest %s into %s" % \
                         (manifest, executable))
    return system(["mt", "-nologo", "-manifest", manifest,
                    f"-outputresource:{executable};1"])

def notify(title, message, alertClass=None):
    CraftCore.debug.step(f"{title}: {message}")
    backends = CraftCore.settings.get("General", "Notify", "")
    if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) or backends == "":
        return
    backends = Notifier.NotificationLoader.load(backends.split(";"))
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
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def createShim(shim, target, args=None, guiApp=False, useAbsolutePath=False) -> bool:
    if not OsUtils.isWin():
        return True
    app = CraftCore.cache.findApplication("shimgen")
    if not app:
        CraftCore.log.error(f"Failed to detect shimgen, please install dev-util/shimgen")
        return False
    if not useAbsolutePath and os.path.isabs(target):
        srcPath = shim
        if srcPath.endswith(".exe"):
            srcPath = os.path.dirname(srcPath)
        target = os.path.relpath(target, srcPath)
    if not os.path.exists(os.path.dirname(shim)):
        os.makedirs(os.path.dirname(shim))
    command = [app, "--output", shim, "--path", target]
    if args:
        command += ["--command", args]
    if guiApp:
        command += ["--gui"]
    return system(command, stdout=subprocess.DEVNULL)


def replaceSymlinksWithCopys(path):
    def resolveLink(path):
        while os.path.islink(path):
            toReplace = os.readlink(path)
            if not os.path.isabs(toReplace):
                path = os.path.join(os.path.dirname(path), toReplace)
            else:
                path = toReplace
        return path

    for root, _, files in os.walk(path):
        for svg in files:
            path = os.path.join(root, svg)
            if os.path.islink(path):
                toReplace = resolveLink(path)
                if not os.path.exists(toReplace):
                    CraftCore.log.error(f"Resolving {path} failed: {toReplace} does not exists.")
                    continue
                if toReplace != path:
                    deleteFile(path)
                    copyFile(toReplace, path)
    return True


def printProgress(percent):
    width, _ = shutil.get_terminal_size((80, 20))
    width -= 20  # margin
    times = int(width / 100 * percent)
    sys.stdout.write(
        "\r[{progress}{space}]{percent}%".format(progress="#" * times, space=" " * (width - times), percent=percent))
    sys.stdout.flush()


class ScopedEnv(object):
    def __init__(self, env):
        self.oldEnv = {}
        for key, value in env.items():
            self.oldEnv[key] = os.environ.get(key, None)
            putenv(key, value)

    def reset(self):
        for key, value in self.oldEnv.items():
            putenv(key, value)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        self.reset()

def normalisePath(path):
    path = os.path.abspath(path)
    if OsUtils.isWin():
        return path.replace("\\", "/")
    return path


def configureFile(inFile : str, outFile : str, variables : dict) -> bool:
    CraftCore.log.debug(f"configureFile {inFile} -> {outFile}\n{variables}")
    configPatter = re.compile(r"@{([^{}]+)}")
    with open(inFile, "rt+") as f:
        script = f.read()
    matches = configPatter.findall(script)
    if not matches:
        CraftCore.log.debug("Nothing to configure")
        return False

    while matches:
        for match in matches:
            val = variables.get(match, None)
            if val is None:
                raise Exception(f"Failed to configure {inFile}: @{match} is not in variables")
            script = script.replace(f"@{{{match}}}", val)
        matches = configPatter.findall(script)

    os.makedirs(os.path.dirname(outFile), exist_ok=True)
    with open(outFile, "wt+") as f:
        f.write(script)
    return True
