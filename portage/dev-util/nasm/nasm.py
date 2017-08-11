import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.11.08'] = "http://www.nasm.us/pub/nasm/releasebuilds/2.11.08/win32/nasm-2.11.08-win32.zip"
        self.targetInstallPath['2.11.08'] = os.path.join("dev-utils", "bin")
        self.targetDigests['2.11.08'] = 'db67cb1286b01e835b703402d631c88c8f494d6b'
        self.targetInstSrc['2.11.08'] = 'nasm-2.11.08'

        self.description = "This is NASM - the famous Netwide Assembler"
        self.defaultTarget = '2.11.08'

    def setDependencies(self):
        self.runtimeDependencies["virtual/bin-base"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
