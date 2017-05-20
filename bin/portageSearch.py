import re

import CraftTimer
from CraftDebug import craftDebug
import portage
import utils
import InstallDB

class SeachPackage(object):
    def __init__(self, package):
        self.category = package.category
        self.subpackage = package.subpackage
        self.package = package.package
        self.homepage = package.subinfo.homepage
        self.shortDescription = package.subinfo.shortDescription
        self.defaultTarget = package.subinfo.defaultTarget


    def __str__(self):
        installed = InstallDB.installdb.getInstalledPackages(self.category, self.package)
        version = None
        revision = None
        if installed:
            if (len(installed)>1):
                raise Exception("Multiple installs are not supported")
            version = installed[0].getVersion() or None
            revision = installed[0].getRevision() or None
        subpackage = f"/{self.subpackage}" if self.subpackage else ""
        return f"""\
{self.category}{subpackage}/{self.package}
    Homepage: {self.homepage}
    Description: {self.shortDescription}
    Latest version: {self.defaultTarget}
    Installed versions: {version}
    Installed revision: {revision}
"""


def packages():
    if not utils.utilsCache.availablePackages:
        utils.utilsCache.availablePackages = []
        craftDebug.log.info("Updating search cache:")
        total = len(portage.PortageInstance.getInstallables())
        for p in portage.PortageInstance.getInstallables():
            pi = portage.PortageInstance.getPackageInstance(p.category, p.package)
            if pi:
                package = SeachPackage(pi)
                utils.utilsCache.availablePackages.append(package)
                percent = int(len(utils.utilsCache.availablePackages)/total * 100)
            utils.printProgress(percent)
        craftDebug.log.info("")
    return utils.utilsCache.availablePackages


def printSearch(search_category, search_package,maxDist = 2):
        with CraftTimer.Timer("Search", 0) as timer:
            similar = []
            match = None
            package_re = re.compile(".*%s.*" % search_package, re.IGNORECASE)
            for package in packages():
                if search_category == "" or search_category == package.category:
                    levDist = utils.levenshtein(search_package.lower(),package.package.lower())
                    if levDist == 0 :
                        match = (levDist,package)
                        break
                    elif package_re.match(package.package):
                        similar.append((levDist-maxDist,package))
                    elif len(package.package)>maxDist and levDist <= maxDist:
                        similar.append((levDist,package))
                    else:
                        if package_re.match(package.shortDescription):
                            similar.append((100,package))

            if match == None:
                if len(similar)>0:
                    print("Craft was unable to find %s, similar packages are:" % search_package)
                    similar.sort( key = lambda x: x[0])
                else:
                    print("Craft was unable to find %s" % search_package)
            else:
                print("Package %s found:" % search_package)
                similar = [match]

            for levDist,package in similar:
                craftDebug.log.debug((package, levDist))
                print(package)
