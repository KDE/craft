import InstallDB
import utils
from Blueprints.CraftPackageObject import *
from Blueprints.CraftVersion import CraftVersion
from Utils import CraftTimer


class SeachPackage(object):
    def __init__(self, package):
        self.path = package.path
        self.name = package.name
        self.webpage = package.subinfo.webpage
        self.description = package.subinfo.description
        self.tags = package.subinfo.tags

        versions = list(package.subinfo.svnTargets.keys()) + list(package.subinfo.targets.keys())
        versions.sort(key=lambda x: CraftVersion(x))
        self.availableVersions = ", ".join(versions)

    @property
    def package(self):
        # we can't cache the whole instance
        out = CraftPackageObject.get(self.path)
        if not out:
            CraftCore.log.error("Cache corrupted")
            CraftCore.cache.clear()
            exit(1)
        return out


    def __str__(self):
        installed = CraftCore.installdb.getInstalledPackages(self.package)
        version = None
        revision = None
        if installed:
            if (len(installed) > 1):
                raise Exception("Multiple installs are not supported")
            version = installed[0].getVersion() or None
            revision = installed[0].getRevision() or None
        latestVersion = self.package.version
        return f"""\
{self.package}
    BlueprintPath: {self.package.source}
    Homepage: {self.webpage}
    Description: {self.description}
    Tags: {self.tags}
    Latest version: {latestVersion}
    Installed versions: {version}
    Installed revision: {revision}

    Available versions: {self.availableVersions}
"""


def packages():
    if not CraftCore.cache.availablePackages:
        CraftCore.cache.availablePackages = []
        CraftCore.log.info("Updating search cache:")
        total = len(CraftPackageObject.installables())
        for p in CraftPackageObject.installables():
            package = SeachPackage(p)
            CraftCore.cache.availablePackages.append(package)
            percent = int(len(CraftCore.cache.availablePackages) / total * 100)
            utils.printProgress(percent)
        utils.printProgress(100)
        CraftCore.log.info("")
    return CraftCore.cache.availablePackages


def printSearch(search_package, maxDist=2):
    searchPackageLower = search_package.lower()
    isPath = "/" in searchPackageLower
    with CraftTimer.Timer("Search", 0) as timer:
        similar = []
        match = None
        package_re = re.compile(f".*{search_package}.*", re.IGNORECASE)
        for searchPackage in packages():
            packageString =  searchPackage.path if isPath else searchPackage.name
            levDist = abs(len(searchPackageLower) - len(packageString))
            if levDist <= maxDist:
                levDist = utils.levenshtein(searchPackageLower, packageString.lower())
            if levDist == 0:
                match = (levDist, searchPackage)
                break
            elif package_re.match(searchPackage.path):
                similar.append((levDist - maxDist, searchPackage))
            elif len(packageString) > maxDist and levDist <= maxDist:
                similar.append((levDist, searchPackage))
            else:
                if package_re.match(searchPackage.description) or \
                        package_re.match(searchPackage.tags):
                    similar.append((100, searchPackage))

        if match == None:
            if len(similar) > 0:
                CraftCore.log.info(f"Craft was unable to find {search_package}, similar packages are:")
                similar.sort(key=lambda x: x[0])
            else:
                CraftCore.log.info(f"Craft was unable to find {search_package}")
        else:
            CraftCore.log.info(f"Package {search_package} found:")
            similar = [match]

        for levDist, searchPackage in similar:
            CraftCore.log.debug((vars(searchPackage), levDist))
            CraftCore.log.info(searchPackage)
