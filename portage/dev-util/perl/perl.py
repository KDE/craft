import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "5.22.1.2201"
        build = "299574"
        arch = "x86-64int"
        if compiler.isX64():
            arch = "x64"
        self.targets[ver] = "http://downloads.activestate.com/ActivePerl/releases/%s/ActivePerl-%s-MSWin32-%s-%s.zip" % (ver, ver, arch, build)
        self.targetDigestUrls[ver] = (["http://downloads.activestate.com/ActivePerl/releases/%s/SHA256SUM" % ver], CraftHash.HashAlgorithm.SHA256)
        self.targetMergeSourcePath[ver] = "ActivePerl-%s-MSWin32-%s-%s\\perl" % (ver, arch, build)
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"

