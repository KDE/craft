# -*- coding: utf-8 -*-
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


# fetch functions

import io
import os
import re
import ssl
import subprocess
import sys
import threading
import urllib
from pathlib import Path

import utils
from CraftCore import CraftCore
from shells import Powershell

try:
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        Progress,
        TextColumn,
        TimeRemainingColumn,
        TransferSpeedColumn,
    )
except ImportError:
    Progress = None


def _richConsole():
    console = CraftCore.debug.console
    if Progress and console and console.is_terminal and not CraftCore.settings.ciMode:
        return console
    return None


def _downloadProgress(console):
    return Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    )


def _contentLength(url) -> int | None:
    cert = CraftCore.standardDirs.etcDir() / "cacert.pem"
    context = ssl.create_default_context(cafile=cert if cert.exists() else None)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=10, context=context) as response:
            return int(response.headers["Content-Length"])
    except Exception as e:
        CraftCore.log.debug(f"Failed to get the size of {url}: {e}")
        return None


def _systemWithProgress(command, url, absFilename: Path) -> bool:
    console = _richConsole()
    if not console:
        return utils.system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    command = [str(x) for x in command]
    CraftCore.log.debug(f"executing command: {command!r}")
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except Exception as e:
        CraftCore.log.error(f"Failed to execute command: {command}: {e}")
        return False
    output = []
    reader = threading.Thread(target=lambda: output.append(proc.stdout.read()), daemon=True)
    reader.start()
    with _downloadProgress(console) as progress:
        task = progress.add_task(absFilename.name, total=None)
        threading.Thread(target=lambda: progress.update(task, total=_contentLength(url)), daemon=True).start()
        while reader.is_alive():
            reader.join(0.2)
            progress.update(task, completed=absFilename.stat().st_size if absFilename.exists() else 0)
    proc.wait()
    log = b"".join(output).decode("utf-8", errors="backslashreplace")
    CraftCore.log.debug(log)
    if proc.returncode != 0:
        CraftCore.log.warning(log)
        CraftCore.log.info(f"Command {command} failed with exit code {proc.returncode}")
        return False
    return True


def getFile(url, destdir, filename="", quiet=None) -> bool:
    """download file from 'url' into 'destdir'"""
    if quiet is None:
        quiet = CraftCore.settings.ciMode
    CraftCore.log.debug("getFile called. url: %s" % url)
    if url == "":
        CraftCore.log.error("fetch: no url given")
        return False

    pUrl = urllib.parse.urlparse(url)
    if not filename:
        filename = os.path.basename(pUrl.path)

    utils.createDir(destdir)

    if pUrl.scheme == "s3":
        return s3File(url, destdir, filename)

    absFilename = Path(destdir) / filename
    # try the other methods as fallback if we are bootstrapping
    bootStrapping = not (CraftCore.standardDirs.etcDir() / "cacert.pem").exists()

    wget2 = CraftCore.cache.findApplication("wget2")
    if wget2 and (not utils.isSystemTool(wget2) or CraftCore.settings.getboolean("Tools", "UseSystemWget", True)):
        if wget2File(wget2, url, destdir, filename, quiet):
            return True
        if not bootStrapping:
            return False

    wget = CraftCore.cache.findApplication("wget")
    if wget and (not utils.isSystemTool(wget) or CraftCore.settings.getboolean("Tools", "UseSystemWget", True)):
        if wgetFile(url, destdir, filename, quiet):
            return True
        if not bootStrapping:
            return False

    curl = CraftCore.cache.findApplication("curl")
    if curl and (not utils.isSystemTool(curl) or CraftCore.settings.getboolean("Tools", "UseSystemCurl", True)):
        if curlFile(url, destdir, filename, quiet):
            return True
        if not bootStrapping:
            return False

    if bootStrapping and absFilename.exists():
        os.remove(absFilename)

    if absFilename.exists():
        return True

    CraftCore.log.info(f"Downloading: {url} to {absFilename}")
    console = _richConsole()
    with _downloadProgress(console) if console else utils.ProgressBar() as progress:
        task = progress.add_task(absFilename.name, total=None) if console else None

        def dlProgress(count, blockSize, totalSize):
            if console:
                progress.update(task, completed=count * blockSize, total=totalSize if totalSize != -1 else None)
            elif totalSize != -1:
                progress.print(int(count * blockSize * 100 / totalSize))
            else:
                sys.stdout.write(("\r%s bytes downloaded" % (count * blockSize)))
                sys.stdout.flush()

        try:
            urllib.request.urlretrieve(
                url,
                filename=absFilename,
                reporthook=dlProgress if CraftCore.debug.verbose() >= 0 else None,
            )
        except Exception as e:
            CraftCore.log.warning(e)
            powershell = Powershell()
            if powershell.pwsh:
                return powershell.execute(
                    [
                        f'[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (new-object net.webclient).DownloadFile("{url}", "{absFilename}")'
                    ]
                )
            return False
    return True


def curlFile(url, destdir, filename, quiet):
    """download file with curl from 'url' into 'destdir', if filename is given to the file specified"""
    curl = CraftCore.cache.findApplication("curl")
    command = [curl, "-C", "-", "--retry", "10", "-L", "--ssl-reqd", "--fail"]
    if timeout := CraftCore.settings.getInt("Tools", "DownloadConnecTimeout", 0):
        command += ["--connect-timeout", timeout]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--cacert", cert]
    # the default of 20 might not be enough for sourceforge ...
    command += ["--max-redirs", "50"]
    command += ["-o", os.path.join(destdir, filename)]
    command += [url]
    CraftCore.log.debug("curlfile called")

    if CraftCore.debug.verbose() < 1:
        if quiet:
            with io.StringIO() as tmp:
                ciMode = CraftCore.settings.ciMode
                if ciMode:
                    command += ["-v"]
                if not utils.system(command, logCommand=ciMode, stdout=tmp, stderr=subprocess.STDOUT):
                    CraftCore.log.warning(tmp.getvalue())
                    return False
                if ciMode:
                    loc = re.findall(r"Host: ([^\s]+)", tmp.getvalue())
                    if loc:
                        CraftCore.log.info(f"Downloaded from: {loc[-1]}")
                return True
        elif CraftCore.cache.checkCommandOutputFor(curl, "--progress-bar", helpCommand="--help all"):
            command += ["--progress-bar"]
        CraftCore.log.info(f"curl {url}")
        return _systemWithProgress(command, url, Path(destdir) / filename)
    command += ["-v"]
    return utils.system(command)


def wgetFile(url, destdir, filename, quiet):
    """download file with wget from 'url' into 'destdir', if filename is given to the file specified"""
    wget = CraftCore.cache.findApplication("wget")
    command = [wget, "--continue", "--tries", "10"]
    if timeout := CraftCore.settings.getInt("Tools", "DownloadConnecTimeout", 0):
        command += [f"--connect-timeout={timeout}"]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--ca-certificate", cert]
    # the default of 20 might not be enough for sourceforge ...
    command += ["--max-redirect", "50"]
    if CraftCore.settings.getboolean("General", "EMERGE_NO_PASSIVE_FTP", False):
        command += ["--no-passive-ftp"]
    if not filename:
        command += ["-P", destdir]
    else:
        command += ["-O", os.path.join(destdir, filename)]
    command += [url]

    if CraftCore.debug.verbose() < 1:
        if quiet:
            with io.StringIO() as tmp:
                ciMode = CraftCore.settings.ciMode
                if not utils.system(command, logCommand=ciMode, stdout=tmp, stderr=subprocess.STDOUT):
                    CraftCore.log.warning(tmp.getvalue())
                    return False
                if ciMode:
                    loc = re.findall(r"Location: ([^\s]+)", tmp.getvalue())
                    if loc:
                        CraftCore.log.info(f"Downloaded from: {loc[-1]}")
                return True
        elif CraftCore.cache.checkCommandOutputFor(wget, "--show-progress"):
            command += ["-q", "--show-progress"]
            CraftCore.log.info(f"wget {url}")
            return _systemWithProgress(command, url, Path(destdir) / filename)
    return utils.system(command)


def wget2File(wgetCommand, url, destdir, filename, quiet):
    """download file with wget from 'url' into 'destdir', if filename is given to the file specified"""
    command = [wgetCommand, "--continue", "--metalink=off"]
    if timeout := CraftCore.settings.getInt("Tools", "DownloadConnecTimeout", 0):
        command += [f"--connect-timeout={timeout}"]
    # the default of 20 might not be enough for sourceforge ...
    # command += ["--max-redirect", "50"]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--ca-certificate", cert]
    if CraftCore.settings.getboolean("General", "EMERGE_NO_PASSIVE_FTP", False):
        command += ["--no-passive-ftp"]
    if not filename:
        command += ["--directory-prefix", destdir]
    else:
        command += ["--output-document", os.path.join(destdir, filename)]
    command += [url]

    if CraftCore.debug.verbose() < 1:
        if quiet:
            with io.StringIO() as tmp:
                ciMode = CraftCore.settings.ciMode
                if not utils.system(command, logCommand=ciMode, stdout=tmp, stderr=subprocess.STDOUT):
                    CraftCore.log.warning(tmp.getvalue())
                    return False
                if ciMode:
                    loc = re.findall(r"([^\s]+)", tmp.getvalue())
                    if loc:
                        CraftCore.log.info(f"Downloaded from: {loc[-1]}")
                return True
        else:
            command += ["-q", "--progress=bar", "--force-progress"]
            CraftCore.log.info(f"wget2 {url}")
            return _systemWithProgress(command, url, Path(destdir) / filename)
    return utils.system(command)


def s3File(url: str, destdir: str, filename: str) -> bool:
    aws = CraftCore.cache.findApplication("aws")
    if not aws:
        CraftCore.log.critical('aws not found, please install awscli. "pip install awscli" ')
        return False
    return utils.system([aws, "s3", "cp", url, os.path.join(destdir, filename)])
