# -*- coding: utf-8 -*-
import subprocess
import tempfile

from CraftDebug import craftDebug
import info
import utils
from Package.MaybeVirtualPackageBase import *
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "2.11.0"
        arch = 32
        if craftCompiler.isX64():
            arch = 64

        self.targets[ver]  ="https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-%s-bit.7z.exe" % (ver, ver, arch)
        self.archiveNames[ver] = "PortableGit-%s-%s-bit.7z" % (ver, arch)
        self.targetInstallPath[ ver ] = os.path.join("dev-utils","git")
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies['dev-util/7zip']   = 'default'


    def gitPostInstall(self):
        git = utils.utilsCache.findApplication("git")
        if utils.utilsCache.checkCommandOutputFor(git, "kde:", "config --global --get url.git://anongit.kde.org/.insteadof"):
            return True
        craftDebug.log.debug("adding kde related settings to global git config file")
        utils.system( f"\"{git}\" config --global url.git://anongit.kde.org/.insteadOf kde:")
        utils.system( f"\"{git}\" config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:")
        utils.system( f"\"{git}\" config --global core.autocrlf false")
        utils.system( f"\"{git}\" config --system core.autocrlf false")

from Package.BinaryPackageBase import *

class GitPackage(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        utils.createShim(os.path.join(self.imageDir(), "dev-utils", "bin", "git.exe"),
                       os.path.join(self.imageDir(), "dev-utils", "git", "bin", "git.exe"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        gitDir = os.path.join( CraftStandardDirs.craftRoot(), "dev-utils", "git")
        utils.system( os.path.join(gitDir, "post-install.bat"), cwd = gitDir)
        self.subinfo.gitPostInstall()
        return True

class GitVirtualPackage(VirtualPackageBase):
    def __init__(self):
        VirtualPackageBase.__init__(self)

    def install( self ):
        self.subinfo.gitPostInstall()
        return VirtualPackageBase.install(self)


class Package(VirtualIfSufficientVersion):
    def __init__(self):
        VirtualIfSufficientVersion.__init__(self, app="git", version="2.10.0", classA=GitPackage, classB=GitVirtualPackage)
