# -*- coding: utf-8 -*-
# this module contains the information class
import datetime
import os

class infoclass:
    def __init__( self, RAW="" ):
        """ """
        self.targets = dict()
        self.targetInstSrc = dict()
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

    # abstract method for setting dependencies, override to set individual targets
    def setDependencies( self ):
        """ """

    # abstract method for setting targets, override to set individual targets
    def setTargets( self ):
        """ """

    # abstract method for setting svn targets, override to set individual targets
    def setSVNTargets( self ):
        """ """

    # return archive file based package url 
    def getPackage( self, repoUrl, name, version, ext='.tar.bz2' ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"

        return repoUrl + '/' + name + '-' + compiler + '-' + version + '-bin' + ext + '\n' + \
               repoUrl + '/' + name + '-' + compiler + '-' + version + '-lib' + ext + '\n'

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
