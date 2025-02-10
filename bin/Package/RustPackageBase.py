# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

from BuildSystem.RustBuildSystem import RustBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.PackagerBase import PackagerBase
from Source.MultiSource import MultiSource


class RustPackageBase(PackageBase, MultiSource, RustBuildSystem, PackagerBase):
    """provides a base class for rust packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("RustPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        RustBuildSystem.__init__(self, **kwargs)
        PackagerBase.__init__(self, **kwargs)

    def fetch(self):
        if self._sourceClass:
            return self._sourceClass.fetch(self)
        return True

    def unpack(self):
        if self._sourceClass:
            return self._sourceClass.unpack(self)
        return True

    def sourceRevision(self):
        if self._sourceClass:
            return self._sourceClass.sourceRevision(self)
        return ""

    # from PackagerBase
    def createPackage(self):
        return True

    def preArchive(self):
        return True
