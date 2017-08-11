import info


class subinfo(info.infoclass):
    def setTargets(self):
        arch = "win32"
        if craftCompiler.isX64():
            arch = "amd64"

        for ver in ["3.5.1", "3.6.0"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/python-{ver}-embed-{arch}.zip"
            self.targetInstallPath[ver] = "python"
        self.defaultTarget = "3.6.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        if not BinaryPackageBase.install(self):
            return False
        # https://bugs.python.org/issue29319
        files = os.listdir(self.installDir())
        reZipName = re.compile(r"python\d\d.*")
        name = None
        for f in files:
            if reZipName.match(f):
                name, _ = os.path.splitext(f)
                break
        return utils.deleteFile(os.path.join(self.installDir(), f"{name}._pth"))
