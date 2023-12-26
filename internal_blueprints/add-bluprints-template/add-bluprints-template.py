# This is a internal recipe
import info
from Blueprints.CraftPackageObject import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValuesFromFile(os.path.join(CraftCore.settings.get("InternalTemp", "add-bluprints-template.ini")))

    def setDependencies(self):
        # make sure core is up to date first
        self.buildDependencies["craft/craft-core"] = None


from Package.BlueprintRepositoryPackageBase import *


class Package(BlueprintRepositoryPackageBase):
    NameRegex = re.compile(r".*[\/:](.+?(?=[\||\:|\.]))")

    def __init__(self):
        BlueprintRepositoryPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        if (
            "InternalTemp",
            "add-bluprints-template.ini",
        ) not in CraftCore.settings or not os.path.exists(CraftCore.settings.get("InternalTemp", "add-bluprints-template.ini")):
            raise BlueprintException(self, "This recipe only works with 'craft --add-blueprint-repository")

    def checkoutDir(self, index=0):
        names = Package.NameRegex.findall(self.repositoryUrl())
        if len(names) != 1:
            CraftCore.log.error(f"Failed to determine the blueprint install folder for {self.repositoryUrl()}")
            return False
        return os.path.join(CraftStandardDirs.blueprintRoot(), names[0])
