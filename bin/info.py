##
#
# @package  this module contains the information class

# the current work here is to access members only
# by methods to be able to separate the access from
# the definition

import datetime
import os
import utils
import compiler
from options import *
import types

class infoclass(object):
    """this module contains the information class"""
    def __init__( self, RAW="" ):
        ### package options
        self.options = Options()
        self.options.readFromEnv()
        self.targets = dict()
        self.archiveNames = dict()
        # Specifiy that the fetched source should be placed into a
        # subdirectory of the default source directory
        self.targetInstSrc = dict()
        # Specifiy that the default source directory should have a suffix after
        # the package name. This is usefull for package which needs different sources.
        self.targetSrcSuffix = dict()
        self.targetConfigurePath = dict()
        self.targetInstallPath = dict()
        self.targetMergeSourcePath = dict()
        self.targetMergePath = dict()

        self.targetDigests = dict()
        self.targetDigestUrls = dict()
        ## \todo prelimary
        self.svnTargets = dict()

        self.hardDependencies = dict()
        self.softDependencies = dict()

        # dependencies is the common way to define dependencies that are both
        # run time and build time dependencies, it is equivalent to hardDependencies
        # runtimeDependencies and buildDependencies are not different when looking
        # at the build process itself, they will only make a difference when getting
        # output of the dependencies
        self.dependencies = dict()
        self.runtimeDependencies = dict()
        self.buildDependencies = dict()

        # a long and a short description for the package
        self.shortDescription = ''
        self.description = ''
        #a url to the projects homepage
        self.homepage = ''
        # the category that will be used in the installer for this package
        # you must only set this property if you want to override the default category
        # of the package
        self.categoryName = ''

        self.patchToApply = dict()  # key: target. Value: list(['patchname', patchdepth]) or ('patchname',patchdepth)
        self.isoDateToday = str( datetime.date.today() ).replace('-', '')
        self.svnTargets['svnHEAD'] = False
        self.svnServer = None       # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self.defaultTarget = 'svnHEAD'
        self.buildTarget = 'svnHEAD'
        self.disableHostBuild = False
        self.disableTargetBuild = False
        self.package = utils.packageSplit(os.path.basename(utils.getCallerFilename()))[0]

        for x in RAW.splitlines():
            if not x == '':
                # if version is not available then set it as -1
                self.hardDependencies[ x ] = [ -1 ]


        self.setDependencies()

        self.setTargets()
        self.setSVNTargets()
        self.setBuildTarget()
        self.setBuildOptions()

    def setDependencies( self ):
        """default method for setting dependencies, override to set individual targets"""

    def setTargets( self ):
        """default method for setting targets, override to set individual targets"""

    def setSVNTargets( self ):
        """default method for setting svn targets, override to set individual targets"""

    def setBuildTarget( self, buildTarget = None):
        """setup current build target"""
        self.buildTarget = self.defaultTarget
        if not buildTarget == None:
            self.buildTarget = buildTarget
        elif not os.getenv( "EMERGE_TARGET" ) == None:
            self.buildTarget = os.getenv( "EMERGE_TARGET" )
        if not self.buildTarget in list(self.targets.keys()) and not self.buildTarget in list(self.svnTargets.keys()) :
            self.buildTarget = self.defaultTarget
            utils.debug("build target %s not defined in available targets %s %s" % (self.buildTarget, list(self.targets.keys()), list(self.svnTargets.keys())), 1)

    def setBuildOptions( self ):
        """default method for setting build options, override to set individual targets"""
        self.disableHostBuild = False
        self.disableTargetBuild = False

    def getPackage( self, repoUrl, name, version, ext='.tar.bz2', packagetypes=None, scheme=None ):
        """return archive file based package url"""
        if packagetypes is None:
            packagetypes = ['bin', 'lib']
        if not os.getenv("EMERGE_PACKAGETYPES") is None:
            packagetypes += os.getenv("EMERGE_PACKAGETYPES").split(',')
        arch = ""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch = "-x64"
        if compiler.isMinGW_W32():
            arch = "-x86"
        compilerName = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compilerName = "mingw"
        elif os.getenv("KDECOMPILER") == "mingw4":
            compilerName = "mingw4"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compilerName = "vc90"
        elif os.getenv("KDECOMPILER") == "msvc2010":
            compilerName = "vc100"
        ret = ''
        # TODO: return '\n'.join(repoUrl + '/' + name + arch + '-' + compilerName + '-' + version + '-' + p + ext for p in packagetypes)
        if scheme == 'sf':
            for packageType in packagetypes:
                ret += repoUrl + '/' + name + '/' + version + '/' + name + arch + '-' + compilerName + '-' + version + '-' + packageType + ext + '\n'
        else:
            for packageType in packagetypes:
                ret += repoUrl + '/' + name + arch + '-' + compilerName + '-' + version + '-' + packageType + ext + '\n'

        return ret

    def packageDigests( self, name, version, ext='.tar.bz2', packagetypes=None ): # pylint: disable=W0613
        """ return archive file based package digests relating to info.infoclass.packageUrls()

The expected digest keys are build in the form <version>[<architecture>]-<compiler>-<packagetype> where
version=<value from version parameter>
compiler='vc90'|'mingw4'
packagetype=<keys from packagestypes parameter>
architecture=<empty for x86>|'-x64'
exception: the mingw-w32 compiler uses x86-mingw4 to not collide with the mingw.org compiler

example:
    # for x86
    self.targetDigests['2.4.2-3-vc90-bin'] = '1b7c2171fb60669924c9d7174fc2e39161f7ef7b'
    self.targetDigests['2.4.2-3-vc90-lib'] = 'e48d8c535cd245bfcc617590d3142035c77b8aa2'
    # for x64
    self.targetDigests['2.4.2-3-x64-vc90-lib'] = 'e48d8c535cd245bfcc617590d3142035c77b8aa2'

    self.targets['2.4.2-3'] = self.packageUrls(repoUrl, "fontconfig", "2.4.2-3")
    self.targetDigests['2.4.2-3'] = self.packageDigests("fontconfig", "2.4.2-3")

        """
        if packagetypes is None:
            packagetypes = ['bin', 'lib']
        if not os.getenv("EMERGE_PACKAGETYPES") is None:
            packagetypes += os.getenv("EMERGE_PACKAGETYPES").split(',')
        arch = ""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch = "-x64"
        if compiler.isMinGW_W32():
            arch = "-x86"
        compilerName = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compilerName = "mingw"
        elif os.getenv("KDECOMPILER") == "mingw4":
            compilerName = "mingw4"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compilerName = "vc90"
        elif os.getenv("KDECOMPILER") == "msvc2010":
            compilerName = "vc100"
        # TODO: use list comprehension
        ret = []
        for packageType in packagetypes:
            key = version + '-' + compilerName + '-' + packageType + arch
            ret.append(self.targetDigests[key])
        return ret

    def getUnifiedPackage( self, repoUrl, name, version, ext='.tar.bz2', packagetypes=None):
        """return archive file based package url for unified packages"""
        if packagetypes is None:
            packagetypes = ['bin', 'lib']
        if not os.getenv("EMERGE_PACKAGETYPES") is None:
            packagetypes += os.getenv("EMERGE_PACKAGETYPES").split(',')
        arch = ""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch = "-x64"
        ret = ''
        for packageType in packagetypes:
            ret += repoUrl + '/' + name + arch + '-' + version + '-' + packageType + ext + '\n'
        return ret

    def getKDEPackageUrl(self, name, version, ext='.tar.bz2', packagetypes=None):
        """return full url of a package provided by the kdewin mirrors"""
        repoUrl = "http://downloads.sourceforge.net/project/kde-windows"
        return self.getPackage( repoUrl, name, version, ext, packagetypes, scheme='sf' )

    def getPackageList( self, baseUrl, files ):
        """returns a package url for multiple files from the same base url"""
        # TODO: replace the entire function by
        # return '\n'.join(baseUrl + '/' + fileName)
        retFiles = ""
        for fileName in files :
            retFiles += baseUrl+'/'+fileName+'\n'
        return retFiles

    def hasTarget( self ):
        """return true if archive targets for the currently selected build target is available"""
        return self.buildTarget in list(self.targets.keys())

    def target( self ):
        """return archive target"""
        if self.buildTarget in list(self.targets.keys()):
            return self.targets[self.buildTarget]
        return ""
    
    def archiveName( self ):
        """returns the archive file name"""
        if self.buildTarget in list(self.archiveNames.keys()):
            return self.archiveNames[self.buildTarget]
        return ""

    def hasMultipleTargets( self ):
        """return whether we used a list of targets"""
        return type( self.targets[self.buildTarget] ) == list

    def targetCount( self ):
        """return the number of targets given either in a list, or split by a space character"""
        if self.hasMultipleTargets():
            return len( self.targets[self.buildTarget] )
        else:
            return len( self.targets[self.buildTarget].split() )

    def targetAt( self, index ):
        """return the specified target at a specific position, or an empty string if out of bounds"""
        if self.targetCount() <= index:
            return ""

        if self.hasMultipleTargets():
            return self.targets[self.buildTarget][index]
        else:
            return self.targets[self.buildTarget].split()[index]

    def hasSvnTarget( self ):
        """return true if version system based target for the currently selected build target is available"""
        return self.buildTarget in list(self.svnTargets.keys())

    def svnTarget( self ):
        """return version system based target for the currently selected build target"""
        if self.buildTarget in list(self.svnTargets.keys()):
            return self.svnTargets[self.buildTarget]
        return ""

    def targetSourceSuffix(self):
        """return local source path suffix for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetSrcSuffix.keys()):
            return self.targetSrcSuffix[ self.buildTarget ]

    def hasTargetSourcePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstSrc.keys())

    def targetSourcePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstSrc.keys()):
            return self.targetInstSrc[ self.buildTarget ]

    def hasConfigurePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetConfigurePath.keys())

    def configurePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) and \
                self.buildTarget in list(self.targetConfigurePath.keys()):
            return self.targetConfigurePath[ self.buildTarget ]

    def hasInstallPath(self):
        """return true if relative path appendable to local install path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstallPath.keys())

    def installPath(self):
        """return relative path appendable to local install path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetInstallPath.keys()):
            return self.targetInstallPath[ self.buildTarget ]
        utils.die("no install path for this build target defined")

    def hasMergePath(self):
        """return true if relative path appendable to local merge path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergePath.keys())

    def mergePath(self):
        """return relative path appendable to local merge path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergePath.keys()):
            return self.targetMergePath[ self.buildTarget ]

    def hasMergeSourcePath(self):
        """return true if relative path appendable to local merge source path is given for the recent target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergeSourcePath.keys())

    def mergeSourcePath(self):
        """return relative path appendable to local merge source path for the recent target"""
        if (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetMergeSourcePath.keys()):
            return self.targetMergeSourcePath[ self.buildTarget ]

    def hasPatches(self):
        """return state for having patches for the recent target"""
        return (len( self.targets ) or len( self.svnTargets )) and self.buildTarget in list(self.patchToApply.keys())

    def patchesToApply(self):
        """return patch informations for the recent build target"""
        if self.hasPatches():
            return self.patchToApply[ self.buildTarget ]
        return ("", "")

    def hasTargetDigests(self):
        """return state if target has digest(s) for the recent build target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetDigests.keys())

    def targetDigest(self):
        """return digest(s) for the recent build target. The return value could be a string or a list"""
        if self.hasTargetDigests():
            return self.targetDigests[ self.buildTarget ]
        return ''

    def hasTargetDigestUrls(self):
        """return state if target has digest url(s) for the recent build target"""
        return (self.buildTarget in list(self.targets.keys()) or self.buildTarget in list(self.svnTargets.keys())) \
                and self.buildTarget in list(self.targetDigestUrls.keys())

    def targetDigestUrl(self):
        """return digest url(s) for the recent build target.  The return value could be a string or a list"""
        if self.hasTargetDigestUrls():
            return self.targetDigestUrls[ self.buildTarget ]
        return ''
