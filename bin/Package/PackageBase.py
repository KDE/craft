#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from EmergeBase import *
from InstallDB import *
from compiler import *

class PackageBase (EmergeBase):
    """
     provides a generic interface for packages and implements the basic stuff for all
     packages
    """

    # uses the following instance variables
    # todo: place in related ...Base

    #rootdir    -> EmergeBase
    #package    -> PackageBase
    #force      -> PackageBase
    #category   -> PackageBase
    #version    -> PackageBase
    #packagedir -> PackageBase
    #imagedir   -> PackageBase

    def __init__(self):
        utils.debug("PackageBase.__init__ called", 2)
        EmergeBase.__init__(self)
        self.setBuildTarget()
        self.forceCreateManifestFiles = False

    def _installedDBPrefix(self, buildType=None):
        postfix = ''
        if buildType == None:
            buildType = self.buildType()
        if self.useBuildTypeRelatedMergeRoot:
            if buildType == 'Debug':
                postfix = 'debug'
            elif buildType == 'Release':
                postfix =  'release'
            elif buildType == 'RelWithDebInfo':
                postfix =  'relwithdebinfo'
        return postfix

    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        self.manifest()
        ## \todo is this the optimal place for creating the post install scripts ?
        # create post install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            # are there any cases there installDir should be honored ?
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                utils.createDir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                utils.copyFile( script, destscript )
        ignoreInstalled = False
        if self.isTargetBuild():
            if installdb.isInstalled( category=None, package=self.package, prefix=os.getenv( "EMERGE_TARGET_PLATFORM" ) ):
                ignoreInstalled = True
                self.unmerge()
        else:
            prefixPath = self._installedDBPrefix( self.buildType() )
            if installdb.isInstalled( category=None, package=self.package, prefix=prefixPath ):
                ignoreInstalled = True
                self.unmerge()

        utils.debug("qmerge package to %s" % self.mergeDestinationDir(), 2)
        utils.mergeImageDirToRootDir( self.mergeSourceDir(), self.mergeDestinationDir() ,utils.envAsBool("EMERGE_USE_SYMLINKS"))

        # run post-install scripts
        if not utils.envAsBool("EMERGE_NO_POST_INSTALL"):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
                script = os.path.join( self.rootdir, "manifest", scriptName )
                if os.path.exists( script ):
                    cmd = "cd /D %s && %s" % ( self.rootdir, script )
                    if not utils.system(cmd):
                        utils.warning("%s failed!" % cmd )
        else:
            utils.debug("running of post-install scripts disabled!", 0)

        # add package to installed database -> is this not the task of the manifest files ?

        # only packages using a specific merge destination path are shared between build types
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            for prefix in [ "Release", "RelWithDebInfo", "Debug" ]:
                if isDBEnabled():
                    package = installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix( prefix ), ignoreInstalled )
                    package.addFiles( utils.getFileListFromManifest(  self._installedDBPrefix( prefix ), self.package ) )
                    package.install()
                else:
                    portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix( prefix ) )
        else:
            if isDBEnabled():
                if emergePlatform.isCrossCompilingEnabled():
                    if self.isTargetBuild():
                        package = installdb.addInstalled( self.category, self.package, self.version,
                                os.getenv( "EMERGE_TARGET_PLATFORM" ), ignoreInstalled )
                    else:
                        package = installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
                    package.addFiles( utils.getFileListFromDirectory( self.mergeSourceDir() ) )
                    package.install()
                else:
                    package = installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix(), ignoreInstalled )
                    package.addFiles( utils.getFileListFromDirectory( self.mergeSourceDir() ) )
                    package.install()
            else:
                portage.addInstalled( self.category, self.package, self.version, self._installedDBPrefix() )

        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        utils.debug( "Packagebase unmerge called", 2 )

        ## \todo mergeDestinationDir() reads the real used merge dir from the
        ## package definition, which fails if this is changed
        ## a better solution will be to save the merge sub dir into
        ## /etc/portage/installed and to read from it on unmerge
        utils.debug( "unmerge package from %s" % self.mergeDestinationDir(), 2 )
        if isDBEnabled():
            if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                    and self.subinfo.options.merge.destinationPath != None:
                for prefix in [ "Release", "RelWithDebInfo", "Debug" ]:
                    packageList = installdb.remInstalled( self.category, self.package, self.version, self._installedDBPrefix( prefix ) )
                    for package in packageList:
                        fileList = package.getFiles()
                        utils.unmergeFileList( self.mergeDestinationDir(), fileList, self.forced )
                        package.uninstall()
            else:
                if self.isTargetBuild():
                    packageList = installdb.remInstalled( self.category, self.package, self.version, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                else:
                    packageList = installdb.remInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
                for package in packageList:
                    fileList = package.getFiles()
                    utils.unmergeFileList( self.mergeDestinationDir(), fileList, self.forced )
                    package.uninstall()
        else:
            if not utils.unmerge( self.mergeDestinationDir(), self.package, self.forced ) and not emergePlatform.isCrossCompilingEnabled():
                # compatibility code: uninstall subclass based package
                utils.unmerge( self.rootdir, self.package, self.forced )
                portage.remInstalled( self.category, self.package, self.version, '')

        # only packages using a specific merge destination path are shared between build types
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix( "Release" ) )
            portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix( "RelWithDebInfo" ) )
            portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix( "Debug" ) )
        else:
            portage.remInstalled( self.category, self.package, self.version, self._installedDBPrefix() )
        return True

    def cleanImage( self ):
        """cleanup before install to imagedir"""
        if self.buildSystemType == 'binary':
            utils.debug("skipped cleaning image dir because we use binary build system", 1)
            return True
        if ( os.path.exists( self.imageDir() ) ):
            utils.debug( "cleaning image dir: %s" % self.imageDir(), 1 )
            utils.cleanDirectory( self.imageDir() )
            os.rmdir(self.imageDir())
        return True

    def cleanBuild( self ):
        """cleanup currently used build dir"""
        if os.path.exists( self.buildDir() ):
            utils.cleanDirectory( self.buildDir() )
            utils.debug( "cleaning build dir: %s" % self.buildDir(), 1 )

        return True

    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers
        install database"""

        utils.debug("base manifest called", 2)
        # important - remove all old manifests to not pollute merge root manifest dir with old packaging info
        utils.cleanManifestDir( self.mergeSourceDir() )
        # For qmerging the manifests files could go into merge destination
        # For packaging they have to stay in image dir
        # ->  the common denominator is to create manifests in image dir
        # qmerge needs creating of manifests and packaging too, there is not need why they are 
        # created in the qmerge step *and* the package step
        # -> merge them into the install step of the build system classes 
        ## @todo move all createManifestFiles() calls into install() method of the Buildsystem classes
        utils.createManifestFiles( self.mergeSourceDir(), self.mergeSourceDir(), self.category, self.package, self.version )
        return True

    def stripLibs( self, pkgName ):
        """strip debugging informations from shared libraries - mingw only!!! """
        return self.strip(pkgName + ".dll" ) 
        
    def strip( self , fileName ):
        """strip debugging informations from shared libraries and executables - mingw only!!! """
        if self.subinfo.options.package.disableStriping or not isMinGW(): 
            utils.debug("Skiping stipping of " + fileName ,2 )
            return True
        basepath = os.path.join( self.installDir() )
        filepath = os.path.join( basepath, "bin",  fileName )

        cmd = "strip -s " + filepath
        utils.debug(cmd,2)
        os.system( cmd )
        return True

    def createImportLibs( self, pkgName ):
        """create the import libraries for the other compiler(if ANSI-C libs)"""
        basepath = os.path.join( self.installDir() )
        utils.createImportLibs( pkgName, basepath )

    def getAction(self, cmd = None ):
        if not cmd:
            command = sys.argv[ 1 ]
            options = None
#            print sys.argv
            if ( len( sys.argv )  > 2 ):
                options = sys.argv[ 2: ]
        else:
            command = cmd
            options = None
        # \todo options are not passed through by emerge.py fix it
        return [command, options]

    def execute( self, cmd=None ):
        """called to run the derived class
        this will be executed from the package if the package is started on its own
        it shouldn't be called if the package is imported as a python module"""

        utils.debug( "EmergeBase.execute called. args: %s" % sys.argv, 2 )
        command, _ = self.getAction(cmd)

        #if self.createCombinedPackage:
        #    oldBuildType = os.environ["EMERGE_BUILDTYPE"]
        #    os.environ["EMERGE_BUILDTYPE"] = "Release"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = "Debug"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = oldBuildType
        #else:
        if self.subinfo.options.disableReleaseBuild and self.buildType() == "Release" \
                or self.subinfo.options.disableDebugBuild and self.buildType() == "Debug":
            print("target ignored for this build type")
            return False

        if emergePlatform.isCrossCompilingEnabled() and self.isHostBuild() and self.subinfo.disableHostBuild \
                and not command == "fetch" and not command == "unpack":
            utils.debug( "host build disabled, skipping host build", 1 )
            return True

        if emergePlatform.isCrossCompilingEnabled() and self.isTargetBuild() and self.subinfo.disableTargetBuild \
                and not command == "fetch" and not command == "unpack":
            utils.debug( "target build disabled, skipping target build", 1 )
            return True

        self.runAction(command)
        return True

    def runAction( self, command ):
        """ \todo TODO: rename the internal functions into the form cmdFetch, cmdCheckDigest etc
        then we get by without this dict:
            ok = getattr(self, 'cmd' + command.capitalize()()
        next we could """
        functions = {"fetch":          "fetch",
                     "cleanimage":     "cleanImage",
                     "cleanbuild":     "cleanBuild",
                     "unpack":         "unpack",
                     "compile":        "compile",
                     "configure":      "configure",
                     "make":           "make",
                     "install":        "install",
                     "test":           "unittest",
                     "qmerge":         "qmerge",
                     "unmerge":        "unmerge",
                     "manifest":       "manifest",
                     "package":        "createPackage",
                     "createpatch":    "createPatch",
                     "geturls":        "getUrls",
                     "printrev":       "sourceVersion",
                     "checkdigest":    "checkDigest",
                     "dumpdeps":       "dumpDependencies"}
        if command in functions:
            ok = getattr(self, functions[command])()
        else:
            ok = utils.error( "command %s not understood" % command )

        if ( not ok ):
            utils.die( "command %s failed" % command )
        return True
