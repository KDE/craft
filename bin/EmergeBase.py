#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
import os
import sys
import datetime
from ctypes import *

import utils
import portage
import compiler
from EmergeConfig import *
import utils


## @todo complete a release and binary merge dir below rootdir
# 1.  enable build type related otDmerge install settings
# 2a. use different install databases for debug and release
# 3. binary packages which are build type independent should be
# marked in both databases or should have a separate install database
# question: How to detect reliable this case ?




class EmergeBase(object):
    """base class for emerge system - holds attributes and methods required by base classes"""

    def __init__( self):
        # TODO: some __init__  of subclasses need to already have been
        # called here. That is really the wrong way round.
        object.__init__(self)
        utils.debug( "EmergeBase.__init__ called", 2 )
        self.filename, self.category, self.package, mod = portage.PortageInstance._CURRENT_MODULE#ugly workaround we need to replace the constructor


        if not hasattr(self, 'subinfo'):
            self.subinfo = mod.subinfo(self)


        if not hasattr(self, 'buildSystemType'):
            self.buildSystemType = None

        # if implicit build time dependency is wanted, depend on internal packages
        # for this class and all of its ancestor classes
        if emergeSettings.getboolean("General", "EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES", False):
            for cls in type(self).mro():
                className = cls.__name__
                packageName = 'internal/%s' % className
                if os.path.exists(os.path.join(EmergeStandardDirs.emergeRoot() , 'emerge', 'portage',
                        'internal', className, '%s-internal.py' % className)):
                    if self.subinfo and not packageName in self.subinfo.buildDependencies:
                        self.subinfo.buildDependencies[packageName] = 'default'

        if hasattr(self,'alreadyCalled'):
            return
        self.alreadyCalled = True

        self.versioned              = False
        self.CustomDefines       = ""
        self.createCombinedPackage  = False

        ## specifies if a build type related root directory should be used
        self.useBuildTypeRelatedMergeRoot = False
        if emergeSettings.getboolean("General","EMERGE_MERGE_ROOT_WITH_BUILD_TYPE", False):
            self.useBuildTypeRelatedMergeRoot = True

        self.isoDateToday           = str( datetime.date.today() ).replace('-', '')


    @property
    def noFetch(self):
        return emergeSettings.getboolean("General", "WorkOffline", False)

    @property
    def noCopy(self):
        return emergeSettings.getboolean("General", "EMERGE_NOCOPY", False)


    @property
    def noFast(self):
        return emergeSettings.getboolean("General", "EMERGE_NOFAST", True )

    @property
    def noClean(self):
        return emergeSettings.getboolean("General", "EMERGE_NOCLEAN", False )

    @property
    def forced(self):
        return emergeSettings.getboolean("General", "EMERGE_FORCED", False )

    @property
    def buildTests(self):
        return emergeSettings.getboolean("General", "EMERGE_BUILDTESTS", False )


    def __adjustPath(self, directory):
        """return adjusted path"""
        if not self.subinfo.options.useShortPathes:
            return directory
        path = c_char_p(directory)
        length = windll.kernel32.GetShortPathNameA(path, 0, 0)
        if length == 0:
            return directory
        buf = create_string_buffer('\000' * (length + 1))
        windll.kernel32.GetShortPathNameA(path, byref(buf), length+1) # ignore function result...
        if utils.verbose() > 0:
            print("converting " + directory + " to " + buf.value)
        return buf.value

    def buildType(self):
        """return currently selected build type"""
        return emergeSettings.get("General","EMERGE_BUILDTYPE")

    def compiler(self):
        """deprecated"""
        """return currently selected compiler"""
        return compiler.getCompilerName()

    def buildArchitecture(self):
        """return the target CPU architecture"""
        compiler.architecture()

    def workDirPattern(self):
        """return base directory name for package related work directory"""
        directory = ""
        if self.subinfo.options.useCompilerType == True:
            directory += "%s-" % compiler.getCompilerName()
        if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
            directory += "ide-"
        if self.subinfo.options.useBuildType == False:
            directory += "%s" % (self.buildTarget)
        elif( self.buildType() == None ):
            directory += "%s-%s" % ("default", self.buildTarget)
        else:
            directory += "%s-%s" % (self.buildType(), self.buildTarget)
        return directory

    def imageDirPattern(self):
        """return base directory name for package related image directory"""
        directory = "image"

        # we assume that binary packages are for all compiler and targets
        ## \todo add image directory support for using binary packages for a specific compiler and build type
        if self.buildSystemType == 'binary':
            return directory

        if self.subinfo.options.useCompilerType == True:
            directory += '-' + compiler.getCompilerName()
        if self.subinfo.options.useBuildType == True:
            directory += '-' + self.buildType()
        directory += '-' + self.buildTarget
        return directory

    def sourceDir(self, dummyIndex=0):
        utils.abstract()

    def packageDir(self):
        """ add documentation """
        return self.__adjustPath( portage.getDirname( self.category, self.package ) )

    def buildRoot(self):
        """return absolute path to the root directory of the currently active package"""
        buildroot    = os.path.join( EmergeStandardDirs.emergeRoot(), "build", self.category, self.package )
        return self.__adjustPath(buildroot)

    def workDir(self):
        """return absolute path to the 'work' subdirectory of the currently active package"""
        _workDir = os.path.join( self.buildRoot(), "work" )
        return self.__adjustPath(_workDir)

    def buildDir(self):
        utils.debug("EmergeBase.buildDir() called", 2)
        builddir = os.path.join(self.workDir(), self.workDirPattern())
        if self.subinfo.options.unpack.unpackIntoBuildDir and self.subinfo.hasTargetSourcePath():
            builddir = os.path.join(builddir, self.subinfo.targetSourcePath())
        utils.debug("package builddir is: %s" % builddir, 2)
        return self.__adjustPath(builddir)

    def imageDir(self):
        """return absolute path to the install root directory of the currently active package
        """
        imageDir =  os.path.join( self.buildRoot(), self.imageDirPattern() )
        return self.__adjustPath(imageDir)

    def installDir(self):
        """return absolute path to the install directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath is used
        """
        if self.subinfo.hasInstallPath():
            installDir = os.path.join( self.imageDir(), self.subinfo.installPath())
        elif self.subinfo.options.install.installPath:
            installDir = os.path.join(self.imageDir(), self.subinfo.options.install.installPath)
        else:
            installDir = self.imageDir()
        return self.__adjustPath(installDir)

    def mergeSourceDir(self):
        """return absolute path to the merge source directory of the currently active package.
        This path may point to a subdir of imageDir() in case @ref info.targetInstallPath for a
        specific target or @ref self.subinfo.options.merge.sourcePath is used
        """
        if self.subinfo.hasMergeSourcePath():
            directory = os.path.join( self.imageDir(), self.subinfo.mergeSourcePath() )
        elif not self.subinfo.options.merge.sourcePath == None:
            directory = os.path.join( self.imageDir(), self.subinfo.options.merge.sourcePath )
        else:
            directory = self.imageDir()
        return self.__adjustPath(directory)

    def mergeDestinationDir(self):
        """return absolute path to the merge destination directory of the currently active package.
        This path may point to a subdir of rootdir in case @ref info.targetMergePath for a specific
        build target or @ref self.subinfo.options.merge.destinationPath is used
        """

        if self.subinfo.hasMergePath():
            directory = os.path.join( EmergeStandardDirs.emergeRoot(), self.subinfo.mergePath() )
        elif not self.subinfo.options.merge.destinationPath == None:
            directory = os.path.join( EmergeStandardDirs.emergeRoot(), self.subinfo.options.merge.destinationPath )
        elif not self.useBuildTypeRelatedMergeRoot or self.subinfo.options.merge.ignoreBuildType:
            directory = EmergeStandardDirs.emergeRoot()
        elif self.buildType() == 'Debug':
            directory = os.path.join(EmergeStandardDirs.emergeRoot(),'debug')
        elif self.buildType() == 'Release':
            directory = os.path.join(EmergeStandardDirs.emergeRoot(),'release')
        elif self.buildType() == 'RelWithDebInfo':
            directory = os.path.join(EmergeStandardDirs.emergeRoot(),'relwithdebinfo')
        else:
            directory = EmergeStandardDirs.emergeRoot()
        return self.__adjustPath(directory)

    def packageDestinationDir( self, withBuildType=True ):
        """return absolute path to the directory where binary packages are placed into.
        Default is to optionally append build type subdirectory"""

        utils.debug( "EmergeBase.packageDestinationDir called", 2 )
        dstpath = emergeSettings.get("General","EMERGE_PKGDSTDIR", "None" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )

        if withBuildType:
            if emergeSettings.getboolean("General", "EMERGE_MERGE_ROOT_WITH_BUILD_TYPE", False ):
                dstpath = os.path.join( dstpath, self.buildType())

        if not os.path.exists(dstpath):
            utils.createDir(dstpath)
        return dstpath

    @property
    def buildTarget(self):
        return self.subinfo.buildTarget

    @property
    def version(self):
        return self.subinfo.defaultTarget

    @property
    def rootdir(self):
        return EmergeStandardDirs.emergeRoot()

    def enterBuildDir(self):
        utils.debug( "EmergeBase.enterBuildDir called", 2 )

        if ( not os.path.exists( self.buildDir() ) ):
            os.makedirs( self.buildDir() )
            if utils.verbose() > 0:
                print("creating: %s" % self.buildDir())

        os.chdir( self.buildDir() )
        if utils.verbose() > 0:
            print("entering: %s" % self.buildDir())

    def enterSourceDir(self):
        if ( not os.path.exists( self.sourceDir() ) ):
            return False
        utils.warning("entering the source directory!")
        os.chdir( self.sourceDir() )
        if utils.verbose() > 0:
            print("entering: %s" % self.sourceDir())

    def system( self, command, errorMessage="", debuglevel=1, **kw):
        """convencience function for running system commands.
        This method prints a debug message and then runs a system command.
        If the system command returns with errors the method prints an error
        message and exits if @ref self.subinfo.options.exitOnErrors  is true"""

        utils.debug( str(command), debuglevel )
        if utils.system( command, **kw):
            return True
        if self.subinfo.options.exitOnErrors:
            utils.warning( "while running %s cmd: %s" % (errorMessage, str(command)) )
        else:
            utils.warning( "while running %s cmd: %s" % (errorMessage, str(command)) )
        return False

    def proxySettings(self):
        host = emergeSettings.get("General", 'EMERGE_PROXY_HOST', "")
        port = emergeSettings.get("General", 'EMERGE_PROXY_PORT', "")
        username = emergeSettings.get("General", 'EMERGE_PROXY_USERNAME', "")
        password = emergeSettings.get("General", 'EMERGE_PROXY_PASSWORD', "")
        return [host, port, username, password]

