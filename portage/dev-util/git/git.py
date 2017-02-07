# -*- coding: utf-8 -*-
import subprocess
import tempfile

from CraftDebug import craftDebug
import info
import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "2.11.1"
        arch = 32
        if compiler.isX64():
            arch = 64

        self.targets[ver]  = f"https://github.com/git-for-windows/git/releases/download/v{ver}.windows.1/MinGit-{ver}-{arch}-bit.zip"
        self.targetInstallPath[ ver ] = os.path.join("dev-utils","git")
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies['dev-util/7zip']   = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        os.makedirs(os.path.join(self.imageDir(),"dev-utils","bin"))
        utils.createBat(os.path.join(self.imageDir(), "dev-utils", "bin", "git.bat"),
                        "%s %%*" % os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "git", "cmd", "git.exe"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        git = os.path.join(self.rootdir,"dev-utils","git","bin","git")
        tmpFile = tempfile.TemporaryFile()
        utils.system( "%s config --global --get url.git://anongit.kde.org/.insteadof" % git,
                      stdout=tmpFile, stderr=subprocess.PIPE  )
        tmpFile.seek( 0 )
        for line in tmpFile:
            if str(line,'UTF-8').find("kde:")>-1:
                return True
        craftDebug.log.debug("adding kde related settings to global git config file")
        utils.system( "%s config --global url.git://anongit.kde.org/.insteadOf kde:" % git)
        utils.system( "%s config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:" % git)
        utils.system( "%s config --global core.autocrlf false" % git)
        utils.system( "%s config --system core.autocrlf false" % git)
        return True

