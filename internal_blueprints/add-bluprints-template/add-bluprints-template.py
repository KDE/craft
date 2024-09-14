# This is a internal recipe
import os
import re

import info
import utils
from Blueprints.CraftPackageObject import BlueprintException
from CraftCore import CraftCore
from CraftStandardDirs import CraftStandardDirs
from Package.BlueprintRepositoryPackageBase import BlueprintRepositoryPackageBase

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValuesFromFile(os.path.join(CraftCore.settings.get("InternalTemp", "add-bluprints-template.ini")))

    def setDependencies(self):
        # make sure core is up to date first
        self.buildDependencies["craft/craft-core"] = None


class Package(BlueprintRepositoryPackageBase):
    NameRegex = re.compile(r".*[\/:]([^.:|\n/]+)")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.disableBinaryCache = True
        if (
            "InternalTemp",
            "add-bluprints-template.ini",
        ) not in CraftCore.settings or not os.path.exists(CraftCore.settings.get("InternalTemp", "add-bluprints-template.ini")):
            raise BlueprintException(self, "This recipe only works with 'craft --add-blueprint-repository")

    def checkoutDir(self, index=0):
        urlParts = utils.splitVCSUrl(self.repositoryUrl())
        names = Package.NameRegex.findall(urlParts[0])
        if len(names) != 1:
            CraftCore.log.error(f"Failed to determine the blueprint install folder for {self.repositoryUrl()}")
            return False
        return os.path.join(CraftStandardDirs.blueprintRoot(), names[0])
