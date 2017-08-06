import info


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "win32"
        if craftCompiler.isX64():
            arch = "amd64"

        self.targets["default"] = ""
        self.defaultTarget = "default"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"
        self.runtimeDependencies["binary/python"] = "default"


from Package.BinaryPackageBase import *
from Package.VirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        utils.cleanDirectory(self.workDir())
        pythonDir = os.path.join(CraftStandardDirs.craftRoot(), "python")
        files = os.listdir(pythonDir)
        reZipName = re.compile(r"python\d\d.*")
        name = None
        for f in files:
            if reZipName.match(f):
                name, _ = os.path.splitext(f)
                break
        os.makedirs(os.path.join(self.sourceDir(), "bin"))
        os.makedirs(os.path.join(self.sourceDir(), "bin", "lib"))
        return utils.unpackFile(pythonDir, f"{name}.zip",
                                os.path.join(self.sourceDir(), "bin", "lib")) \
               and utils.copyFile(os.path.join(pythonDir, f"{name}.dll"), os.path.join(self.sourceDir(), "bin"), False)

    def install(self):
        return BinaryPackageBase.install(self)
