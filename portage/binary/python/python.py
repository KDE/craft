import info


class subinfo(info.infoclass):
    def setTargets( self ):
        arch = "win32"
        if compiler.isX64():
            arch = "amd64"

        for ver in ["3.5.1", "3.6.0"]:
            self.targets[ver] = f"https://www.python.org/ftp/python/{ver}/python-{ver}-embed-{arch}.zip"
            self.targetInstallPath[ver] = "python"
        self.defaultTarget = "3.6.0"

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
