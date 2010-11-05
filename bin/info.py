## 
#
# @package  this module contains the information class

# the current work here is to access members only 
# by methods to be able to separate the access from 
# the definition 

import datetime
import os
import utils
from options import *

class infoclass:
    def __init__( self, RAW="" ):
        """ """
        ### package options
        self.options = Options()
        self.targets = dict()
        """Specifiy that the fetched source should be placed into a 
        subdirectory of the default source directory"""
        self.targetInstSrc = dict()
        """Specifiy that the default source directory should have a suffix after 
        the package name. This is usefull for package which needs different sources."""
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
        self.longDescription = ''
        self.description = ''
        # the category that will be used in the installer for this package
        self.categoryName = ''

        self.patchToApply = dict()  # list ( 'patchname', patchdepth for patch )
        self.isoDateToday = str( datetime.date.today() ).replace('-', '')
        self.svnTargets['svnHEAD'] = False
        self.svnServer = None       # this will result in the use of the default server (either anonsvn.kde.org or svn.kde.org)
        self.defaultTarget = 'svnHEAD'
        self.buildTarget = 'svnHEAD'
        
        for x in RAW.splitlines():
            if not x == '':
                """ if version is not available then set it as -1 """
                self.hardDependencies[ x ] = [ -1 ]
        

        self.setDependencies()
        
        self.setTargets()
        self.setSVNTargets()
        self.setBuildTarget()
        self.setBuildOptions()

    # abstract method for setting dependencies, override to set individual targets
    def setDependencies( self ):
        """ """

    # abstract method for setting targets, override to set individual targets
    def setTargets( self ):
        """ """

    # abstract method for setting svn targets, override to set individual targets
    def setSVNTargets( self ):
        """ """

    # setup current build target
    def setBuildTarget( self, buildTarget = None):
        self.buildTarget = self.defaultTarget
        if not buildTarget == None:
            self.buildTarget = buildTarget
        elif not os.getenv( "EMERGE_TARGET" ) == None:
            self.buildTarget = os.getenv( "EMERGE_TARGET" )
        if not self.buildTarget in self.targets.keys() and not self.buildTarget in self.svnTargets.keys() :
            self.buildTarget = self.defaultTarget
            utils.debug("build target %s not defined in available targets %s %s" % (self.buildTarget, self.targets.keys(), self.svnTargets.keys()), 1)

    # abstract method for setting build options, override to set individual targets
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = False

    # return archive file based package url 
    def getPackage( self, repoUrl, name, version, ext='.tar.bz2', packagetypes=['bin', 'lib'] ):
        arch=""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch="-x64"
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "mingw4":
            compiler = "mingw4"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"
        elif os.getenv("KDECOMPILER") == "msvc2010":
            compiler = "vc100"
        ret=''
        for type in packagetypes:
            ret += repoUrl + '/' + name + arch + '-' + compiler + '-' + version + '-' + type + ext + '\n'
        return ret

    def packageDigests( self, name, version, ext='.tar.bz2', packagetypes=['bin', 'lib'] ):
        """ return archive file based package digests relating to info.infoclass.packageUrls()

The expected digest keys are build in the form <version>[<architecture>]-<compiler>-<packagetype> where 
version=<value from version parameter>
compiler='vc90'|'mingw4'
packagetype=<keys from packagestypes parameter>
architecture=<empty for x86>|'-x64'

example: 
    # for x86 
    self.targetDigests['2.4.2-3-vc90-bin'] = '1b7c2171fb60669924c9d7174fc2e39161f7ef7b'
    self.targetDigests['2.4.2-3-vc90-lib'] = 'e48d8c535cd245bfcc617590d3142035c77b8aa2'
    # for x64 
    self.targetDigests['2.4.2-3-x64-vc90-lib'] = 'e48d8c535cd245bfcc617590d3142035c77b8aa2'

    self.targets['2.4.2-3'] = self.packageUrls(repoUrl, "fontconfig", "2.4.2-3")
    self.targetDigests['2.4.2-3'] = self.packageDigests("fontconfig", "2.4.2-3")

        """
        arch=""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch="-x64"
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "mingw4":
            compiler = "mingw4"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"
        elif os.getenv("KDECOMPILER") == "msvc2010":
            compiler = "vc100"
        ret=[]
        for type in packagetypes:
            key = version + '-' + compiler + '-' + type + arch
            ret.append(self.targetDigests[key])
        return ret

    #return archive file based package url for unified packages
    def getUnifiedPackage( self, repoUrl, name, version, ext='.tar.bz2', packagetypes=['bin', 'lib'] ):
        arch=""
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
            arch="-x64"
        ret=''
        for type in packagetypes:
            ret += repoUrl + '/' + name + arch + '-' + version + '-' + type + ext + '\n'
        return ret
               
    #returns a package url for multiple files from the same base url
    def getPackageList( self , baseUrl , files ):
       retFiles=""
       for file in files :
          retFiles += baseUrl+'/'+file+'\n'
       return retFiles               

    # return true if archive targets for the currently selected build target is available
    def hasTarget( self ):
        return self.buildTarget in self.targets.keys()
        
    # return archive target
    def target( self ):
        if self.buildTarget in self.targets.keys():
            return self.targets[self.buildTarget]
        return ""

    # return true if version system based target for the currently selected build target is available
    def hasSvnTarget( self ):
        return self.buildTarget in self.svnTargets.keys()
        
    # return version system based target for the currently selected build target
    def svnTarget( self ):
        if self.buildTarget in self.svnTargets.keys():
            return self.svnTargets[self.buildTarget]
        return ""

    def targetSourceSuffix(self):
        """return local source path suffix for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetSrcSuffix.keys():
            return self.targetSrcSuffix[ self.buildTarget ]

    def hasTargetSourcePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstSrc.keys()
            
    def targetSourcePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstSrc.keys():
            return self.targetInstSrc[ self.buildTarget ]
        
    def hasConfigurePath(self):
        """return true if relative path appendable to local source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetConfigurePath.keys()
            
    def configurePath(self):
        """return relative path appendable to local source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetConfigurePath.keys():
            return self.targetConfigurePath[ self.buildTarget ]

    def hasInstallPath(self):
        """return true if relative path appendable to local install path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstallPath.keys()
                
    def installPath(self):
        """return relative path appendable to local install path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetInstallPath.keys():
            return self.targetInstallPath[ self.buildTarget ]
        utils.die("no install path for this build target defined")
            
    def hasMergePath(self):
        """return true if relative path appendable to local merge path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergePath.keys()
                
    def mergePath(self):
        """return relative path appendable to local merge path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergePath.keys():
            return self.targetMergePath[ self.buildTarget ]

    def hasMergeSourcePath(self):
        """return true if relative path appendable to local merge source path is given for the recent target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergeSourcePath.keys()
                
    def mergeSourcePath(self):
        """return relative path appendable to local merge source path for the recent target"""
        if (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetMergeSourcePath.keys():
            return self.targetMergeSourcePath[ self.buildTarget ]

    def hasPatches(self):
        """return state for having patches for the recent target"""
        return (len( self.targets ) or len( self.svnTargets )) and self.buildTarget in self.patchToApply.keys()
        
    def patchesToApply(self):
        """return patch informations for the recent build target"""
        if self.hasPatches():
            return self.patchToApply[ self.buildTarget ]
        return ("","")

    def hasTargetDigests(self):
        """return state if target has digest(s) for the recent build target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetDigests.keys()

    def targetDigest(self):
        """return digest(s) for the recent build target. The return value could be a string or a list"""
        if self.hasTargetDigests():
            return self.targetDigests[ self.buildTarget ]
        return ''

    def hasTargetDigestUrls(self):
        """return state if target has digest url(s) for the recent build target"""
        return (self.buildTarget in self.targets.keys() or self.buildTarget in self.svnTargets.keys()) and self.buildTarget in self.targetDigestUrls.keys()

    def targetDigestUrl(self):
        """return digest url(s) for the recent build target.  The return value could be a string or a list"""
        if self.hasTargetDigestUrls():
            return self.targetDigestUrls[ self.buildTarget ]
        return ''
