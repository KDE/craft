from .CollectionPackagerBase import *
from .PortablePackager import *
from .NullsoftInstallerPackager import *


class MultiCollectionPackager(PortablePackager, NullsoftInstallerPackager):
    @InitGuard.init_once
    def __init__(self, whitelists=None, blacklists=None):
        PortablePackager.__init__(self, whitelists, blacklists)
        NullsoftInstallerPackager.__init__(self, whitelists, blacklists)

    def createPackage(self):
        if "setupname" in self.defines:
            CraftCore.log.error("MultiCollectionPackager doesn't support a custome setupname")
            return False

        if not self.isNsisInstalled():
            return False
        self.internalCreatePackage()

        # redist is directly included by libs/runtime
        self.defines["vcredist"] = "none"
        self.generateNSISInstaller()
        destDir, archiveName = os.path.split(self.defines["setupname"])
        self._generateManifest(destDir, archiveName)
        CraftHash.createDigestFiles(self.defines["setupname"])

        del self.defines["setupname"]
        self.createPortablePackage()
        CraftHash.createDigestFiles(self.defines["setupname"])
        return True
