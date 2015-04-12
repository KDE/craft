import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "5.20.2.2001"
        build = "298913"
        arch = "x86-64int"
        if compiler.isX64():
            arch = "x64"
            self.targetDigests['5.20.2.2001'] = '91e37d112c58659f14063c541efeefee3499046f'
        else:
            self.targetDigests['5.20.2.2001'] = '5b51bbb4e06c0850dfe76814e775224ee235dcbb'
        self.targets[ver] = "http://downloads.activestate.com/ActivePerl/releases/%s/ActivePerl-%s-MSWin32-%s-%s.zip" % (ver, ver, arch, build)
        self.targetMergeSourcePath[ver] = "ActivePerl-%s-MSWin32-%s-%s\\perl" % (ver, arch, build)
        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

