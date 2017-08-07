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


def printPackagesForFileSearch(filename):
    packages = InstallDB.installdb.getPackagesForFileSearch(filename)
    for pId, filename in packages:
        category, packageName, version = pId.getPackageInfo()
        craftDebug.log.info("%s/%s: %s" % (category, packageName, filename))
