import glob
from xml.etree import ElementTree as et

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/indilib/indi.git"
        self.description = 'INDI Library'
        self.defaultTarget = 'master'
        self.targetInstSrc['master'] = "libindi"

    def setDependencies(self):
        self.buildDependencies["gnuwin32/grep"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["win32libs/libnova"] = "default"
        self.runtimeDependencies["win32libs/cfitsio"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DINDI_BUILD_SERVER=OFF -DINDI_BUILD_DRIVERS=OFF -DINDI_BUILD_CLIENT=ON -DINDI_BUILD_QT5_CLIENT=OFF"

    # Need to copy all drivers XML files manually since indiserver and drivers are not built on Windows
    def install(self):
        dest = os.path.join(self.installDir(), "bin", "data", "indi")
        if not os.path.exists(dest):
            os.makedirs(dest)
        # File all drivers XML files including *.xml.cmake template files
        rootDir = self.sourceDir()[:-7]
        # Root directory of indiclient tree
        globSearch = rootDir + '**\*.xml*'
        for filename in glob.iglob(globSearch, recursive=True):
            if not ("_sk" in filename):
                if filename.endswith(".cmake"):
                    destFilename = os.path.basename(filename)
                    destFilename = dest + '\\' + destFilename[:-6]
                    # Rename .xml.cmake to .xml and copy it to destination. NO LINKS
                    utils.copyFile(filename, destFilename, False)
                    xmlFile = destFilename
                    tree = et.parse(destFilename)
                    root = tree.getroot()
                    # Set all version to 1.0 for now
                    for version in root.iter('version'):
                        version.text = '1.0'
                    tree.write(destFilename)
                # Regular .xml file get copied directly
                else:
                    utils.copyFile(filename, dest)
        return CMakePackageBase.install(self)
