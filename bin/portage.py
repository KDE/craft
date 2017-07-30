## @package portage
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import builtins
import importlib

import datetime

import InstallDB
import utils
from CraftConfig import *
from CraftDebug import craftDebug
from CraftDependencies import DependencyType, PortageException, DependencyPackage
from CraftPackageObject import PackageObjectBase
from CraftVersion import CraftVersion


class Portage(object):
    #cache for pacages
    _rootDirCache = dict()
    _packageDict = dict()
    options = ""

    def __init__( self ):
        """ """
        self.categories = {}
        self.subpackages = {}
        self.portages = {}
        self._CURRENT_MODULE = ()#todo refactor package constructor
        self.ignores = re.compile("a^")
        if ("Portage", "Ignores") in craftSettings:
            self.ignores = Portage.generateIgnoreList(craftSettings.get("Portage", "Ignores").split(";"))

    @staticmethod
    def generateIgnoreList(ignores):
        return re.compile("(%s)" % "|".join( ["^%s$" % entry for entry in ignores]))

    @staticmethod
    def buildType():
        """return currently selected build type"""
        return craftSettings.get("Compile", "BuildType")

    @staticmethod
    def rootDirectories():
        # this function should return all currently set portage directories
        if ("General", "Portages") in craftSettings:
            rootDirs = craftSettings.get("General", "Portages").split(";")
        else:
            rootDirs = []
        if len(rootDirs) == 0:
            rootDirs = [CraftStandardDirs.craftRepositoryDir()]
        return rootDirs

    @staticmethod
    def rootDirForCategory(category):
        """this function should return the portage directory where it finds the first occurance of the category

    throws exception if not found
    """
        # this function should return the portage directory where it finds the
        # first occurance of a category or the default value
        for i in Portage.rootDirectories():
            if category and os.path.exists(os.path.join(i, category)):
                return i
        craftDebug.log.critical("can't find category %s" % category)

    @staticmethod
    def rootDirForPackage(category, package):
        """returns the portage directory where it finds the first occurance of this package
    """
        name = "%s/%s" % (category, package)
        if not name in Portage._rootDirCache:
            for i in Portage.rootDirectories():
                if os.path.exists(os.path.join(i, category, package)):
                    Portage._rootDirCache[name] = i
        return Portage._rootDirCache[name]

    @staticmethod
    def getFullPackage(package):
        """tries to find a package and returns either category / subpackage / package or category / package

    returns an empty list if not found
    """
        category = PortageInstance.getCategory(package)
        if not category: return []
        if package in PortageInstance.subpackages:
            _cat, subpackage = PortageInstance.subpackages[package][0].split('/')
            if not _cat == category: return []
            return [category, subpackage, package]
        else:
            return [category, package]

    @staticmethod
    def getDirname(category, package):
        """ return absolute pathname for a given category and package """
        subpackage, package = PortageInstance.getSubPackage(category, package)
        if category and package:
            if subpackage:
                return os.path.join(Portage.rootDirForPackage(category, subpackage), category, subpackage, package)
            else:
                return os.path.join(Portage.rootDirForPackage(category, package), category, package)
        else:
            craftDebug.log.critical("broken category or package %s/%s" % (category, package))

    @staticmethod
    def getFilename(category, package):
        """ return absolute filename for a given category, package  """
        return os.path.join(Portage.getDirname(category, package), "%s.py" % package)

    @staticmethod
    def VCSDirs():
        return ['.svn', 'CVS', '.hg', '.git']

    def addPortageDir( self, directory ):
        """ adds the categories and packages of a portage directory """
        if not os.path.exists( directory ):
            return

        categoryList = os.listdir( directory )

        # remove vcs directories
        for vcsdir in Portage.VCSDirs():
            if vcsdir in categoryList:
                categoryList.remove( vcsdir )
        if "__pycache__" in categoryList:
            categoryList.remove( "__pycache__" )

        self.portages[ directory ] = []
        for category in categoryList:
            if not os.path.isdir( os.path.join( directory, category ) ):
                continue

            self.portages[ directory ].append( category )

            packageList = os.listdir( os.path.join( directory, category ) )

            # remove vcs directories
            for vcsdir in Portage.VCSDirs():
                if vcsdir in packageList:
                    packageList.remove( vcsdir )
            if "__pycache__" in packageList:
                packageList.remove( "__pycache__" )

            if not category in list(self.categories.keys()):
                self.categories[ category ] = []

            for package in packageList:
                if not os.path.isdir( os.path.join( directory, category, package ) ):
                    continue
                if not package in self.categories[ category ]:
                    subpackage, package = self.getSubPackage(category, package)
                    self.categories[ category ].append( PackageObjectBase(category=category, subpackage=subpackage, package=package ) )

                subPackageList = os.listdir( os.path.join( directory, category, package ) )

                # remove vcs directories
                for vcsdir in Portage.VCSDirs():
                    if vcsdir in subPackageList:
                        subPackageList.remove( vcsdir )
                if "__pycache__" in subPackageList:
                    subPackageList.remove( "__pycache__" )

                for subPackage in subPackageList:
                    if not os.path.isdir( os.path.join( directory, category, package, subPackage ) ) or subPackage in Portage.VCSDirs():
                        continue

                    if not subPackage in self.subpackages:
                        self.subpackages[ subPackage ] = []
                        self.categories[ category ].append( PackageObjectBase( category=category, subpackage=package, package=subPackage ) )
                    self.subpackages[ subPackage ].append( category + "/" + package )

    def getCategory( self, package ):
        """ returns the category of this package """
        craftDebug.log.debug("getCategory: %s" % package)

        for cat in self.categories:
            if package in self.categories[ cat ]:
                craftDebug.log.debug("getCategory: found category %s for package %s" % (cat, package))
                return cat
        return False

    def isCategory( self, category ):
        """ returns whether a certain category exists """
        return category in self.categories

    def isPackage( self, category, package ):
        """ returns whether a certain package exists within a category """
        return package in self.categories[ category ]

    def isVirtualPackage( self, category, package ):
        """ check if that package is of VirtualPackageBase """
        if not self.isPackage( category, package ):
            return False
        mod = self.getPackageInstance(category,package)
        for baseClassObject in mod.__class__.__bases__:
            if baseClassObject.__name__ == 'VirtualPackageBase': return True
        return False


    def getAllPackages( self, category ):
        """returns all packages of a category
        in case the category doesn't exist, nothing is returned"""
        if self.isCategory( category ):
            return self.categories[ category ]
        else:
            return []

    def getPackageInstance(self, category, package):
        """return instance of class Package from package file"""
        fileName =  Portage.getFilename( category, package )
        pack = None
        mod = None
        if fileName.endswith(".py") and os.path.isfile(fileName):
            if not fileName in self._packageDict:
                craftDebug.log.debug("module to import: %s" % fileName)
                if not os.path.isfile( fileName ):
                    try:
                        mod = builtins.__import__( fileName )
                    except ImportError as e:
                        craftDebug.log.warning('import failed for module %s: %s' % (fileName, str(e)))
                        mod =  None
                else:
                    modulename = os.path.basename( fileName )[:-3].replace('.', '_')
                    loader = importlib.machinery.SourceFileLoader(modulename, fileName)
                    try:
                        mod = loader.load_module()
                    except Exception as e:
                        raise PortageException("Failed to load file %s" % fileName, category, package, e)
                if not mod is None:
                    subpackage, package = self.getSubPackage( category, package )
                    self._CURRENT_MODULE  = ( fileName, category,subpackage, package, mod )
                    pack = mod.Package( )
                    self._packageDict[ fileName ] = pack
                else:
                    raise PortageException("Failed to find package", category, package)
            else:
                pack = self._packageDict[ fileName ]
            return pack

    def getDefaultTarget( self, category, package ):
        """ returns the default package of a specified package """
        craftDebug.log.debug("getDefaultTarget: importing file %s" % Portage.getFilename(category, package))
        if not ( category and package ):
            return dict()

        info = self._getSubinfo( category, package )
        if not info is None:
            if info.options.dailyUpdate and info.hasSvnTarget():
                return str(datetime.date.today()).replace("-", ".")
            return info.defaultTarget
        else:
            return None

    def getAllTargets( self, category, package ):
        """ returns all targets of a specified package """
        craftDebug.log.debug("getAllTargets: importing file %s" % Portage.getFilename(category, package))
        if not ( category and package ):
            return dict()
        info = self._getSubinfo( category, package )
        if not info is None:
            tagDict = info.svnTargets.copy()
            tagDict.update( info.targets )
            craftDebug.log.debug(tagDict)
            return tagDict
        else:
            return dict()

    def getAllVCSTargets( self, category, package ):
        """ returns all version control system targets of a specified package,
            excluding those which do contain tags """
        craftDebug.log.debug("getAllVCSTargets: importing file %s" % Portage.getFilename(category, package))
        info = self._getSubinfo(  category, package )
        if not info is None:
            tagDict = info.svnTargets
            for key in tagDict:
                craftDebug.log.debug('%s: %s' % (key, tagDict[key]))
            return tagDict
        else:
            return dict()

    def getUpdatableVCSTargets( self, category, package ):
        """ check if the targets are tags or not """
        targetDict = PortageInstance.getAllVCSTargets( category, package )
        retList = []
        for key in targetDict:
            url = targetDict[ key ]
            if url:
                sourceType = utils.getVCSType( url )
                if sourceType == "svn":
                    # for svn, ignore tags
                    if not url.startswith( "tags/" ) and not "/tags/" in url:
                        retList.append( key )
                elif sourceType == "git":
                    _, branch, tag = utils.splitVCSUrl( url )
                    if tag == "" and not branch.endswith("-patched"):
                        retList.append( key )
                elif not sourceType == "":
                    # for all other vcs types, simply rebuild everything for now
                    retList.append( key )
        return retList

    def getNewestVersion( self, category, package ):
        """ returns the newest version of this category/package """
        if( category == None ):
            raise PortageException("Empty category", category, package)
        if not self.isCategory( category ):
            raise PortageException("Could not find category", category, package)
        if not self.isPackage( category, package ):
            raise PortageException("Could not find package", category, package)

        installed = InstallDB.installdb.getInstalledPackages(category, package)
        newest = PortageInstance.getDefaultTarget( category, package )

        for pack in installed:
            version = pack.getVersion()
            if not version or not newest: continue
            if CraftVersion(newest) < CraftVersion(version):
                newest = version
        return newest

    def getInstallables( self ):
        """ get all the packages that are within the portage directory """
        instList = list()
        for category in list(self.categories.keys()):
            for package in self.categories[ category ]:
                instList.append(package)
        return instList

    def getSubPackage(self, category, package):
        """ returns package and subpackage names """
        """ in case no subpackage could be found, None is returned """
        if package in PortageInstance.subpackages:
            for entry in PortageInstance.subpackages[package]:
                cat, pac = entry.split("/")
                if cat == category: return pac, package
        return None, package

    def _getSubinfo(self, category, package):
        pack = self.getPackageInstance(category, package)
        if pack:
            return pack.subinfo
        return None

# when importing this, this static Object should get added
PortageInstance = Portage()
PackageObjectBase.PortageInstance = PortageInstance#we can't include that file due to circlic dependencies...
for _dir in Portage.rootDirectories():
    PortageInstance.addPortageDir( _dir )


def solveDependencies(category, package, depType = DependencyType.Both, maxDepth = -1, ignoredPackages = None):
    if ( category == "" ):
        category = PortageInstance.getCategory( package )
        craftDebug.log.debug("found package in category %s" % category)

    pac = DependencyPackage(category, package)
    return pac.getDependencies(depType=depType, maxDepth = maxDepth, ignoredPackages = ignoredPackages )

def isPackageUpdateable( category, package ):
    craftDebug.log.debug("isPackageUpdateable: importing file %s" % Portage.getFilename(category, package))
    subinfo = PortageInstance._getSubinfo( category, package )
    if not subinfo is None:
        if len( subinfo.svnTargets ) == 1 and not subinfo.svnTargets[ list(subinfo.svnTargets.keys())[0] ]:
            return False
        return len( subinfo.svnTargets ) > 0
    else:
        return False

def printCategoriesPackagesAndVersions(lines):
    """prints a number of 'lines', each consisting of category, package and version field"""
    def printLine( cat, pack, ver, hnt="" ):
        catlen = 25
        packlen = 25
        craftDebug.log.info(cat + " " * ( catlen - len( cat ) ) + pack + " " * ( packlen - len( pack ) ) + ver + hnt)

    printLine( 'Category', 'Package', 'Version' )
    printLine( '--------', '-------', '-------' )
    for category, package, version in lines:
        printLine( category, package, version )

def printPackagesForFileSearch(filename):
    packages = InstallDB.installdb.getPackagesForFileSearch(filename)
    for pId, filename in packages:
        category, packageName, version = pId.getPackageInfo()
        craftDebug.log.info("%s/%s: %s" % (category, packageName, filename))

def getPackagesCategories(packageName, defaultCategory = None):
    craftDebug.trace("getPackagesCategories for package name %s" % packageName)
    if defaultCategory is None:
        defaultCategory = craftSettings.get("General","EMERGE_DEFAULTCATEGORY","kde")

    packageList, categoryList = [], []
    split = packageName.split( "/" )
    if len( split ) == 1:
        if PortageInstance.isCategory( packageName ):
            craftDebug.log.debug("isCategory=True")
            packages = PortageInstance.getAllPackages( packageName )
            # TODO: directly return the package...
            for p in packages:
                categoryList.append(p.category)
                packageList.append(p.package)
        else:
            craftDebug.log.debug("isCategory=False")
            if PortageInstance.isCategory( defaultCategory ) and PortageInstance.isPackage( defaultCategory, packageName ):
                # prefer the default category
                packageList = [ packageName ]
                categoryList = [ defaultCategory ]
            else:
                if PortageInstance.getCategory( packageName ):
                    packageList = [ packageName ]
                    categoryList = [ PortageInstance.getCategory( packageName ) ]
    elif 2 <= len( split ) <= 3:
        if len(split) == 3:
            cat, sub, pac = split
        else:
            cat, pac = split
        if PortageInstance.isCategory( cat ):
            categoryList = [ cat ]
        else:
            return packageList, categoryList
        if len( categoryList ) > 0 and PortageInstance.isPackage( categoryList[0], pac ):
            packageList = [ pac ]
        if len( categoryList ) and len( packageList ):
            craftDebug.log.debug("added package %s/%s" % (categoryList[0], pac))
    else:
        craftDebug.log.error("unknown packageName")

    uniqeCategories = set(categoryList)
    if len(uniqeCategories) > 1:
        craftDebug.log.error(f"Package clash detected:  packages:{packageList}, categories: {uniqeCategories}")
        #todo: return value instead of list
    return packageList, categoryList
