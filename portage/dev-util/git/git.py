# -*- coding: utf-8 -*-
import subprocess
import tempfile

from CraftDebug import craftDebug
import info
import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "2.11.0"
        arch = 32
        if compiler.isX64():
            arch = 64

        self.targets[ver]  ="https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-%s-bit.7z.exe" % (ver, ver, arch)
        self.archiveNames[ver] = "PortableGit-%s-%s-bit.7z" % (ver, arch)
        self.targetInstallPath[ ver ] = os.path.join("dev-utils","git")
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies['dev-util/7zip']   = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.gitIsInstalled = False
        if utils.utilsCache.checkVersionGreaterOrEqual("git", version="2.10.0"):
            self.gitIsInstalled = True

    def fetch(self):
        if self.gitIsInstalled:
            return True
        return BinaryPackageBase.fetch(self)

    def unpack(self):
        if self.gitIsInstalled:
            return True
        return BinaryPackageBase.unpack(self)

    def install( self ):
        if self.gitIsInstalled:
            return True
        if not BinaryPackageBase.install(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(), "git.exe"),
                       os.path.join(self.imageDir(), "dev-utils", "bin", "git.exe"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        if not self.gitIsInstalled:
            utils.system( "cmd /C post-install.bat", cwd = os.path.join( CraftStandardDirs.craftRoot(), "dev-utils", "git"))
        git = utils.utilsCache.findApplication("git")
        if utils.utilsCache.checkCommandOutputFor(git, "kde:", "config --global --get url.git://anongit.kde.org/.insteadof"):
            return True
        craftDebug.log.debug("adding kde related settings to global git config file")
        utils.system( f"\"{git}\" config --global url.git://anongit.kde.org/.insteadOf kde:")
        utils.system( f"\"{git}\" config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:")
        utils.system( f"\"{git}\" config --global core.autocrlf false")
        utils.system( f"\"{git}\" config --system core.autocrlf false")
        return True

