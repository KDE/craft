from Package.BinaryPackageBase import *
import os
import info
import utils
import subprocess

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['latest'] = \
                """http://files.kolab.org/local/windows-ce/gpg_wince-dev-latest.zip"""
        self.targetDigests['20100823'] = "34a922ac947e90828cae9ad471ca6ae56495b1dd"
        self.targets['20100823'] = \
                """http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg_wince-dev-230810.zip"""
        self.targetDigests['20100826'] = "ff6c1d6b0ac663e08cba28ac96d1f7e17c223da1"
        self.targets['20100826'] = \
                """http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg_wince-dev-260810.zip"""
        self.targetDigests['20101011'] = "164dfb1bbb62db1e23bf80bcbb46338b6c95df2c"
        self.targets['20101011'] = \
        self.targets['20101021'] = (
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg_wince-dev-211010.zip "
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg-msc-dev.zip")
        self.targets['20101115'] = (
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg_wince-dev-151110.zip "
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg-msc-dev-151110.zip")
        self.targets['20101117'] = (
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg_wince-dev-171110.zip "
                "http://files.kolab.org/local/windows-ce/gpg-snapshots/gpg-msc-dev-171110.zip")
        self.defaultTarget = '20101117'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

    def execute(self):
        (command, option) = self.getAction()
        if command == "install":
            self.runAction(command)
            utils.debug("Generating libgpgme.lib", 2)
            deffile = os.path.join(self.imageDir(), "lib", "gpgme.def")
            outfile = os.path.join(self.imageDir(), "lib", "libgpgme.lib")
            args = ["lib", "/machine:thumb", "/name:libgpgme-11",
                    "/out:%s" % outfile, "/def:%s" %deffile]
            return subprocess.call(args) == 0
        else:
            return self.runAction(command) == 0


if __name__ == '__main__':
    Package().execute()
