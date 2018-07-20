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

from CraftCore import CraftCore
from CraftDebug import deprecated
import utils

import os
import urllib
import subprocess
import sys


@deprecated("Utils.GetFiles.getFile")
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

    pUrl = urllib.parse.urlparse(url)
    if not filename:
        filename = os.path.basename(pUrl.path)

    if pUrl.scheme == "s3":
      s3File(url, destdir, filename)

    # curl and wget basically only work when we have a cert store on windows
    if not CraftCore.compiler.isWindows or os.path.exists(os.path.join(CraftCore.standardDirs.etcDir(), "cacert.pem")):
        if CraftCore.cache.findApplication("wget"):
            return wgetFile(url, destdir, filename)

        if CraftCore.cache.findApplication("curl"):
            return curlFile(url, destdir, filename)

    if os.path.exists(os.path.join(destdir, filename)):
        return True

    powershell = CraftCore.cache.findApplication("powershell")
    if powershell:
        filename = os.path.join(destdir, filename)
        return utils.system([powershell, "-NoProfile", "-ExecutionPolicy", "ByPass", "-Command",
                       f"(new-object net.webclient).DownloadFile(\"{url}\", \"{filename}\")"])
    else:
        def dlProgress(count, blockSize, totalSize):
            if totalSize != -1:
                percent = int(count * blockSize * 100 / totalSize)
                utils.printProgress(percent)
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
    command += ["-o", os.path.join(destdir, filename)]
    command += [url]
    CraftCore.log.debug("curlfile called")

    if not CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False) and CraftCore.debug.verbose() < 1 and CraftCore.cache.checkCommandOutputFor(curl, "--progress-bar"):
        command += ["--progress-bar"]
        CraftCore.log.info(f"curl {url}")
        return utils.system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    else:
        if CraftCore.debug.verbose() > 0:
            command += ["-v"]
        return utils.system(command)


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
        return utils.system(command, displayProgress=True, logCommand=False, stderr=subprocess.STDOUT)
    else:
        return utils.system(command)

def s3File(url, destdir, filename):
    aws = CraftCore.cache.findApplication("aws")
    if not aws:
        CraftCore.log.critical("aws not found, please install awscli. \"pip install awscli\" ")
        return False
    return utils.system([aws, "s3", "cp", url, os.path.join(destdir, filename)])
