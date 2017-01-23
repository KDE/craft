import info


class subinfo(info.infoclass):
    def setTargets( self ):
        "http://downloads.activestate.com/ActivePerl/releases/5.24.1.2402/ActivePerl-5.24.1.2402-MSWin32-x64-401627.exe"
        ver = "5.24.1.2402"
        build = "401627"
        arch = "x86-64int"
        if compiler.isX64():
            arch = "x64"
        self.targets[ver] = "http://downloads.activestate.com/ActivePerl/releases/{ver}/ActivePerl-{ver}-MSWin32-{arch}-{build}.exe".format(
            ver=ver, arch=arch, build=build)
        self.targetInstallPath[ver] = "dev-utils"
        self.targetInstSrc[ver] = "6235264" #TODO: where is the number coming from ....
        self.targetDigestUrls[ver] = (["http://downloads.activestate.com/ActivePerl/releases/{0}/SHA256SUM".format(ver)], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.unpack.runInstaller = True
        self.subinfo.options.configure.defines = "/extract {0}".format(self.workDir())


    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        _, name = os.path.split(self.subinfo.targets[self.subinfo.buildTarget])
        utils.deleteFile(os.path.join(self.sourceDir(), "{0}.msi".format(name)))
        return True

