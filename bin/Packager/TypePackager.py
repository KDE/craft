# -*- coding: utf-8 -*-
# Copyright (c) 2015 Patrick Spendrin <ps_ml@gmx.de>
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

from Packager.CreateArchivePackager import *
from Packager.MacDMGPackager import *
from Packager.MSIFragmentPackager import *
from Packager.NullsoftInstallerPackager import *
from Packager.PortablePackager import *
from Packager.SevenZipPackager import *
from Packager.QtIFPackager import *


class TypePackager(PackagerBase):
    """packager that is used in place of different other packagers
The packager used can be decided at runtime
"""

    def __init__(self, defaultType=CraftCore.settings.get("Packager", "PackageType", "")):
        if not defaultType:
            if CraftCore.compiler.isWindows:
                defaultType = NullsoftInstallerPackager
            elif CraftCore.compiler.isMacOS:
                defaultType = MacDMGPackager
            else:
                defaultType = SevenZipPackager
        elif isinstance(defaultType, str):
            defaultType = eval(defaultType)
        CraftCore.log.debug("TypePackager __init__ %s" % defaultType)
        self.__packager = None
        self.changePackager(defaultType)

    def changePackager(self, packager=None):
        if not packager == None and ("Packager", "PackageType") in CraftCore.settings:
            CraftCore.log.debug(
                "Packager setting %s overriten by with %s" % (packager, CraftCore.settings.get("Packager", "PackageType")))
            packager = eval(CraftCore.settings.get("Packager", "PackageType"))

        if packager == None:
            return

        if self.__packager:
            bases = list(self.__class__.__bases__)
            for i in range(len(bases)):
                if bases[i] == self.__packager:
                    CraftCore.log.info(f"Replace Packager: {bases[i]} with {packager}")
                    bases[i] = packager
            self.__class__.__bases__ = tuple(bases)
        else:
            self.__class__.__bases__ += (packager,)
        packager.__init__(self)
        self.__packager = packager

    def createPackage(self):
        return self.__packager.createPackage(self)
