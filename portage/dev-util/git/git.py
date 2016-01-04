# -*- coding: utf-8 -*-
import tempfile

import EmergeDebug
import info
import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "2.6.4"
        arch = 32
        if compiler.isX64():
            arch = 64
           
        self.targets[ver]  ="https://github.com/git-for-windows/git/releases/download/v%s.windows.1/PortableGit-%s-%s-bit.7z.exe" % (ver, ver, arch)
        self.archiveNames[ver] = "PortableGit-%s-%s-bit.7z" % (ver, arch)
        self.defaultTarget = ver

    def setDependencies(self):
        self.buildDependencies['dev-util/7zip']   = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils//git";
        self.subinfo.options.merge.ignoreBuildType = True

    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        utils.copyFile(os.path.join(self.packageDir(),"git.exe"),os.path.join(self.rootdir,"dev-utils","bin","git.exe"))
        utils.copyFile(os.path.join(self.packageDir(),"git.sh"),os.path.join(self.rootdir,"dev-utils","bin","git"))#bash script
        utils.copyFile(os.path.join(self.packageDir(),"gb.bat"),os.path.join(self.rootdir,"dev-utils","bin","gb.bat"))
        utils.copyFile(os.path.join(self.packageDir(),"gitk.bat"),os.path.join(self.rootdir,"dev-utils","bin","gitk.bat"))
        utils.copyFile(os.path.join(self.packageDir(),"vi.bat"),os.path.join(self.rootdir,"dev-utils","bin","vi.bat"))
        utils.copyFile(os.path.join(self.packageDir(),"vim.bat"),os.path.join(self.rootdir,"dev-utils","bin","vim.bat"))
        return True

    def qmerge(self):
        if not BinaryPackageBase.qmerge(self):
            return False
        gitbash = os.path.join(self.rootdir, "dev-utils", "git", "git-bash.exe")
        utils.system( "%s --no-needs-console --hide --no-cd --command=post-install.bat" % gitbash, cwd = os.path.join( EmergeStandardDirs.emergeRoot(), "dev-utils", "git"))
        tmpFile = tempfile.TemporaryFile()
        git = os.path.join(self.rootdir,"dev-utils","git","bin","git")
        utils.system( "%s config --global --get url.git://anongit.kde.org/.insteadof" % git,
                      stdout=tmpFile, stderr=tmpFile  )
        tmpFile.seek( 0 )
        for line in tmpFile:
            if str(line,'UTF-8').find("kde:")>-1:
                return True
        EmergeDebug.debug("adding kde related settings to global git config file", 1)
        utils.system( "%s config --global url.git://anongit.kde.org/.insteadOf kde:" % git)
        utils.system( "%s config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:" % git)
        utils.system( "%s config --global core.autocrlf false" % git)
        utils.system( "%s config --system core.autocrlf false" % git)
        return True

