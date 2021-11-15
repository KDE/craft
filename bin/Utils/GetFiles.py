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


### fetch functions

from genericpath import exists
from CraftCore import CraftCore
from CraftDebug import deprecated
import utils
from shells import Powershell

import io
import os
from pathlib import Path
import urllib
import subprocess
import sys
import re

def getFile(url, destdir, filename='', quiet=None) -> bool:
    """download file from 'url' into 'destdir'"""
    if quiet is None:
        quiet = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)
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
    elif pUrl.scheme == "minio":
        return minioGet(pUrl.netloc + pUrl.path, destdir, filename)

    absFilename = Path(destdir) / filename
    # try the other methods as fallback if we are bootstrapping
    bootStrapping = not (CraftCore.standardDirs.etcDir() / "cacert.pem").exists()
    if not CraftCore.settings.getboolean("General", "NoWget"):
        if CraftCore.cache.findApplication("wget"):
            if not wgetFile(url, destdir, filename, quiet) and not bootStrapping:
                return False

    if CraftCore.cache.findApplication("curl"):
        if not curlFile(url, destdir, filename, quiet) and not bootStrapping:
            return False

    if bootStrapping and absFilename.exists():
        os.remove(absFilename)

    if absFilename.exists():
        return True

    CraftCore.log.info(f"Downloading: {url} to {absFilename}")
    with utils.ProgressBar() as progress:
        def dlProgress(count, blockSize, totalSize):
            if totalSize != -1:
                progress.print(int(count * blockSize * 100 / totalSize))
            else:
                sys.stdout.write(("\r%s bytes downloaded" % (count * blockSize)))
                sys.stdout.flush()

        try:
            urllib.request.urlretrieve(url, filename=absFilename,
                                    reporthook=dlProgress if CraftCore.debug.verbose() >= 0 else None)
        except Exception as e:
            CraftCore.log.warning(e)
            powershell =  Powershell()
            if powershell.pwsh:
                return powershell.execute([f"[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (new-object net.webclient).DownloadFile(\"{url}\", \"{absFilename}\")"])
            return False
    return True


def curlFile(url, destdir, filename, quiet):
    """download file with curl from 'url' into 'destdir', if filename is given to the file specified"""
    curl = CraftCore.cache.findApplication("curl")
    command = [curl, "-C", "-", "--retry", "10", "-L", "--ftp-ssl", "--fail"]
    cert = os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")
    if os.path.exists(cert):
        command += ["--cacert", cert]
    # the default of 20 might not be enough for sourceforge ...
    command += ["--max-redirs",  "50"]
    command += ["-o", os.path.join(destdir, filename)]
    command += [url]
    CraftCore.log.debug("curlfile called")

    if CraftCore.debug.verbose() < 1:
        if quiet:
            with io.StringIO() as tmp:
                ciMode = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)
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
        elif CraftCore.cache.checkCommandOutputFor(curl, "--progress-bar"):
            command += ["--progress-bar"]
            CraftCore.log.info(f"curl {url}")
            return utils.system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    command += ["-v"]
    return utils.system(command)


def wgetFile(url, destdir, filename, quiet):
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

    if CraftCore.debug.verbose() < 1:
        if quiet:
            with io.StringIO() as tmp:
                ciMode = CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False)
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
            return utils.system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    return utils.system(command)

def s3File(url : str, destdir : str, filename : str) ->bool:
    aws = CraftCore.cache.findApplication("aws")
    if not aws:
        CraftCore.log.critical("aws not found, please install awscli. \"pip install awscli\" ")
        return False
    return utils.system([aws, "s3", "cp", url, os.path.join(destdir, filename)])

def minioGet(url : str, destdir : str, filename : str) ->bool:
    minio = None
    if CraftCore.compiler.isWindows:
        minio = CraftCore.cache.findApplication("minio")
    if not minio:
        minio = CraftCore.cache.findApplication("mc")
    if not minio:
        CraftCore.log.critical("minio client not found, please install minio")
        return False
    return utils.system([minio, "cp", url, os.path.join(destdir, filename)])
