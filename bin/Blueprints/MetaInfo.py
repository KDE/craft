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

import os

from VersionInfo import VersionInfo

class MetaInfo(object):
    """Wrapper for infoclass and CategoryPackageObject"""
    def __init__(self, package):
        self.__package = package

    @property
    def _versionInfo(self):
        if not hasattr(self, "__versionInfo"):
            if self.__package.isCategory():
                path = os.path.join(self.__package.filePath, "version.ini")
                if os.path.exists(path):
                    self.__versionInfo = VersionInfo(package=self.__package, fileName=path)
                else:
                    self.__versionInfo = None
            else:
                self.__versionInfo = None
        return self.__versionInfo

    def __get(self, name):
        out = None
        if not self.__package.isCategory():
            out = getattr(self.__package.subinfo, name)
        if not out:
            out = getattr(self.__package.categoryInfo, name)
        return out

    @property
    def description(self):
        return self.__get("description")

    @property
    def displayName(self):
        return self.__get("displayName")

    @property
    def webpage(self):
        return self.__get("webpage")

    @property
    def tags(self):
        return self.__get("tags")

    @property
    def versions(self):
        if self.__package.isCategory():
            if self._versionInfo:
                return self._versionInfo.tags() + self._versionInfo.tarballs() + self._versionInfo.branches()
        else:
            return list(self.__package.subinfo.svnTargets.keys()) + list(self.__package.subinfo.targets.keys())
        return []

