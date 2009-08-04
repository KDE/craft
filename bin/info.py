# -*- coding: utf-8 -*-
# this module contains the information class

# the current work here is to access members only 
# by methods to be able to separate the access from 
# the definition 

import datetime
import os
import utils

## prelimary settings/options support 
# not clear if it would be better to use 
# class orientated settings like PackagerSettings 
# or action orientated settings like 
# actions.package
# -> I guess action orientated settings would be much better 

class ActionPackageOptions:
    def __init__(self):
        ## defines the package name 
        self.packageName = ""
        ## use compiler in package name
        self.withCompiler = True
        ## use special packaging mode  (only for qt)
        self.specialMode = False
        ## pack also sources 
        self.packSources = True

class ActionConfigureOptions:
    def __init__(self):
        ## configure defines 
        self.defines = ""
        ## subdir based in sourceDir() in which the main build system related config file is located 
        self.configurePath = ""

class Options:
	def __init__(self):
		self.configure = ActionConfigureOptions()
		self.package = ActionPackageOptions()


class infoclass:
    def __init__( self, RAW="" ):
        """ """
        self.options = Options()
        self.targets = dict()
        self.targetInstSrc = dict()
        self.targetConfigurePath = dict()
        self.targetInstallPath = dict()
        self.targetMergeSourcePath = dict()
        self.targetMergePath = dict()
        ## \todo prelimary 
        self.svnTargets = dict()
        self.hardDependencies = dict()
        self.softDependencies = dict()
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
        else:
            utils.debug( "setting buildtarget to " + self.buildTarget, 2 )
    
    # return archive file based package url 
    def getPackage( self, repoUrl, name, version, ext='.tar.bz2' ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"

        return repoUrl + '/' + name + '-' + compiler + '-' + version + '-bin' + ext + '\n' + \
               repoUrl + '/' + name + '-' + compiler + '-' + version + '-lib' + ext + '\n'

    # return archive file based package url for unified packages
    def getUnifiedPackage( self, repoUrl, name, version, ext='.tar.bz2' ):
        return repoUrl + '/' + name + '-' + version + '-bin' + ext + '\n' + \
               repoUrl + '/' + name + '-' + version + '-lib' + ext + '\n'

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

    def patchesToApply(self):
        """return patch informations for the recent build target"""
        if len( self.targets ) and self.buildTarget in self.patchToApply.keys():
            return self.patchToApply[ self.buildTarget ]
        return ("","")
