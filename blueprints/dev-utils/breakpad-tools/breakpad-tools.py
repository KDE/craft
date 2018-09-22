import info
import os
import shutil

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    """We use Jon Turney's fork which adds support for MinGW and a python script to fetch deps"""
    def setTargets(self):
        for ver in ["pecoff-dwarf-on-git-20171117-fetch-externals-on-win"]:
            self.svnTargets[ver] = f"[git]https://github.com/dschmidt/google-breakpad|{ver}|"
            self.patchToApply[ver] = [("0001-Add-CMake-script-to-build-dump_syms.patch", 1)]

        self.defaultTarget = 'pecoff-dwarf-on-git-20171117-fetch-externals-on-win'
        self.description = "The tools part of the breakpad crash-reporting system."
        self.webpage = "https://github.com/dschmidt/google-breakpad"

    def setDependencies(self):
        self.buildDependencies["dev-utils/python2"] = "default"


class Package(CMakePackageBase):
    def fetch(self):
        if not super().fetch():
            return False

        utils.system(["python2", "fetch-externals"], cwd=self.sourceDir())

        return True
