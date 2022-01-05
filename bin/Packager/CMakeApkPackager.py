import os

from Packager.PackagerBase import PackagerBase
from CraftCore import *
from CraftBase import InitGuard
from Utils.Arguments import Arguments
import utils


import glob
from xml.etree import ElementTree

class CMakeApkPackager(PackagerBase):
    @InitGuard.init_once
    def __init__(self):
        PackagerBase.__init__(self)
        self.__androidApkTargets = set()
        self.__androidApkDirs = set()

    @property
    def androidApkDirs(self):
        self.androidApkTargets
        return self.__androidApkDirs

    @property
    def androidApkTargets(self):
        """Android APK parameter auto-detection,
           see https://invent.kde.org/sysadmin/ci-tooling/-/blob/master/system-images/android/sdk/get-apk-args.py"""
        if not self.__androidApkTargets:
            files = glob.iglob(f"{self.sourceDir()}/**/AndroidManifest.xml*", recursive=True)
            for file in files:
                if "3rdparty" in file or "examples" in file or "tests" in file:
                    continue
                tree = ElementTree.parse(file)
                prefix = '{http://schemas.android.com/apk/res/android}'
                for md in tree.findall("application/activity/meta-data"):
                    if md.attrib[prefix + 'name'] == 'android.app.lib_name':
                        targetName = md.attrib[prefix + 'value']
                        if not targetName in self.__androidApkTargets:
                            self.__androidApkTargets.add(targetName)
                            self.__androidApkDirs.add(os.path.dirname(file))
        return self.__androidApkTargets

    def createPackage(self):
        if self.androidApkTargets:
            self.enterBuildDir()
            command = Arguments.formatCommand([self.makeProgram], ["create-apk"])
            return utils.system(command)
        CraftCore.log.critical("Failed to detect package target")
        return False
