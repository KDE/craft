# -*- coding: utf-8 -*-
import tempfile

import info
import utils


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "1.9.5-preview20141217"
        self.targets['1.9.5']  ="https://github.com/msysgit/msysgit/releases/download/Git-%s/PortableGit-%s.7z" % (ver, ver)
        self.targetDigests['1.9.5'] = '19c755a0679cd7801594b4d2dd53dde3ca1dc5b9'
        self.defaultTarget = '1.9.5'

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
        tmpFile = tempfile.TemporaryFile()
        git = os.path.join(self.rootdir,"dev-utils","git","bin","git")
        utils.system( "%s config --global --get url.git://anongit.kde.org/.insteadof" % git,
            stdout=tmpFile, stderr=tmpFile  )
        tmpFile.seek( 0 )
        for line in tmpFile:
            if str(line,'UTF-8').find("kde:")>-1:
                return True
        utils.debug( "adding kde related settings to global git config file",1 )
        utils.system( "%s config --global url.git://anongit.kde.org/.insteadOf kde:" % git)
        utils.system( "%s config --global url.ssh://git@git.kde.org/.pushInsteadOf kde:" % git)
        utils.system( "%s config --global core.autocrlf false" % git)
        utils.system( "%s config --system core.autocrlf false" % git)
        return True

