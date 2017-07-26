#!/usr/bin/env python
from collections import OrderedDict

from CraftDebug import craftDebug


class PackageObjectBase(object):
    PortageInstance = None

    def __init__(self, category, subpackage, package, version = None):
        self.category = category
        self.subpackage = subpackage
        self.package = package
        self._version = version
        self._fullName = "/".join(self._signature())


    def _signature(self):
        if self.subpackage:
            return self.category, self.subpackage, self.package
        else:
            return self.category, self.package


    def fullName(self):
        return self._fullName

    @property
    def version(self):
        if not self._version:
            self._version = PackageObjectBase.PortageInstance.getNewestVersion(self.category, self.package)
        return self._version

    def __eq__(self, other):
        if isinstance(other, PackageObjectBase):
            return other._signature() == self._signature()
        if isinstance(other, str):
            if other == self.package:
                return True
            if other == self.fullName():
                return True
        return False

    def __str__(self):
        return self.fullName()

    def __hash__(self):
        return self._signature().__hash__()
