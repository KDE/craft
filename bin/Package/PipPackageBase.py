import io
from email.parser import HeaderParser

import utils
from BuildSystem.PipBuildSystem import PipBuildSystem
from CraftCore import CraftCore
from Package.PackageBase import PackageBase
from Packager.TypePackager import TypePackager
from Source.MultiSource import MultiSource


class PipPackageBase(PackageBase, MultiSource, PipBuildSystem, TypePackager):
    """provides a base class for pip packages"""

    def __init__(self, **kwargs):
        CraftCore.log.debug("PipPackageBase.__init__ called")
        PackageBase.__init__(self, **kwargs)
        MultiSource.__init__(self, **kwargs)
        PipBuildSystem.__init__(self, **kwargs)
        TypePackager.__init__(self, **kwargs)

        self.pipPackageName = self.package.name

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
        with io.StringIO() as tmp:
            if not utils.system(["python3", "-m", "pip", "show", self.pipPackageName], stdout=tmp):
                return ""
            return HeaderParser().parsestr(tmp.getvalue().strip())["Version"]
