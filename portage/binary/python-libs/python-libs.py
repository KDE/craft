import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "3.6.0"
        arch = "win32"
        if compiler.isX64():
            arch = "amd64"
        self.targets[ver] = "https://www.python.org/ftp/python/%s/python-%s-embed-%s.zip" % (ver, ver, arch)
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)

    def install(self):
        success = utils.unpackFile(self.workDir(), "python36.zip", self.workDir() + "/lib/")
        if not success: return False
        success = utils.copyFile(self.workDir() + "/python36.dll",
                                 self.imageDir() + "/bin/python35.dll")
        if not success: return False
        utils.copyDir(self.workDir() + "/lib/", self.imageDir() + "/bin/lib/")
        return True

