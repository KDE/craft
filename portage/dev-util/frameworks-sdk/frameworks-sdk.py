import info
import utils
import InstallDB
from EmergeConfig import EmergeStandardDirs as esd
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.targets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )

    def fetch(self):
        return True

    def unpack(self):
        return True

    def removeCategoryFromDB(self, category):
        list = self.db.getDistinctInstalled(category)
        for c,p,_ in list:
            for package in self.db.getInstalledPackages( c, p ):
                package.uninstall()



    def resetSettings(self, settingsFile):
        with open(settingsFile, "rt+") as fin:
            text = fin.read()
        def _replaceSetting(reg, new, text):
            return re.compile(reg, re.MULTILINE).sub(new, text)
        text = _replaceSetting("^PACKAGE_IGNORES.*$", "PACKAGE_IGNORES =", text)
        text = _replaceSetting("^EMERGE_USE_CCACHE.*$", "#EMERGE_USE_CCACHE = True", text)
        text = _replaceSetting("^Python =.*$", "Python = C:\python34", text)
        text = _replaceSetting("^DOWNLOADDIR =.*$", "#DOWNLOADDIR = C:\kde\download", text)
        with open(settingsFile, "wt+") as fout:
            fout.write(text)

    def install(self):
        """ we have the whole logic here """
        imageEtcDir = os.path.join(self.imageDir(), "etc")
        installDBFile = os.path.join(imageEtcDir, "install.db")
        settingsFile = os.path.join(imageEtcDir, "kdesettings.ini")
        if os.path.exists(self.imageDir()):
            utils.cleanDirectory(self.imageDir())
        os.makedirs(imageEtcDir)
        # get the current installdb and the kdesettings.ini file
        utils.copyFile(os.path.join(EmergeStandardDirs.etcPortageDir(), "install.db"), installDBFile, linkOnly=False)
        utils.copyFile(os.path.join(EmergeStandardDirs.etcDir(), "kdesettings.ini"), settingsFile, linkOnly=False)
        self.resetSettings(settingsFile)
        self.db = InstallDB(installDBFile)
        self.removeCategoryFromDB("gnuwin32")
        self.removeCategoryFromDB("dev-util")
        # FIXME: the kdesettings file still contains packages that are not part of the frameworks sdk!!!
        return True

    def qmerge(self):
        return True

