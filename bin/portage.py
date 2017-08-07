## @package portage
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import builtins
import datetime
import importlib

import InstallDB
import utils
from CraftConfig import *
from CraftDebug import craftDebug
from CraftPackageObject import CraftPackageObject, DependencyType, PortageException, DependencyPackage
from CraftVersion import CraftVersion

def getNewestVersion(package):
    """ returns the newest version of this /package """
    installed = InstallDB.installdb.getInstalledPackages(package)
    newest = package.version

    for pack in installed:
        version = pack.getVersion()
        if not version or not newest: continue
        if CraftVersion(newest) < CraftVersion(version):
            newest = version
    return newest

def printCategoriesPackagesAndVersions(installed):
    """prints a number of 'lines', each consisting of category, package and version field"""
    width = 40
    def printLine(first, second):
        craftDebug.log.info(f"{first:{width}}: {second}")

    printLine("Package", "Version")
    printLine("=" * width, "=" * 10)
    installed = [(CraftPackageObject.get(x), y) for x, y in installed]
    installed = sorted(installed, key=lambda x :x[0].path)
    for package, version in installed:
        printLine(package.path, version)


def printPackagesForFileSearch(filename):
    packages = InstallDB.installdb.getPackagesForFileSearch(filename)
    for pId, filename in packages:
        category, packageName, version = pId.getPackageInfo()
        craftDebug.log.info("%s/%s: %s" % (category, packageName, filename))
