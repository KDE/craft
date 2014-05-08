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
        ## \todo is this the optimal place for creating the post install scripts ?
        ignoreInstalled = False

        prefixPath = self._installedDBPrefix( self.buildType() )
        if installdb.isInstalled( category=None, package=self.package, prefix=prefixPath ):
            ignoreInstalled = True
            self.unmerge()

        

        utils.debug("qmerge package to %s" % self.mergeDestinationDir(), 2)
        utils.mergeImageDirToRootDir( self.mergeSourceDir(), self.mergeDestinationDir() )

        # run post-install scripts
        if not emergeSettings.getboolean("General","EMERGE_NO_POST_INSTALL", False ):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-install-%s-%s.cmd" % ( self.package, pkgtype )
                script = os.path.join( self.mergeDestinationDir(), "manifest", scriptName )
                if os.path.exists( script ):
                    utils.debug("run post install script '%s'" % script , 2)
                    cmd = "cd /D %s && %s" % ( self.mergeDestinationDir(), script )
                    if not utils.system(cmd):
                        utils.warning("%s failed!" % cmd )
                else:
                    utils.debug("post install script '%s' not found" % script , 2)
        else:
            utils.debug("running of post install scripts disabled!", 0)

        # add package to installed database -> is this not the task of the manifest files ?

        # only packages using a specific merge destination path are shared between build types
        revision = self.sourceVersion()
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            for prefix in [ "Release", "RelWithDebInfo", "Debug" ]:
                package = installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix( prefix ), ignoreInstalled, revision = revision)
                package.addFiles( utils.getFileListFromDirectory(  self._installedDBPrefix( prefix ) ) )
                package.install()
        else:
            package = installdb.addInstalled( self.category, self.package, self.version, self._installedDBPrefix(), ignoreInstalled, revision = revision )
            package.addFiles( utils.getFileListFromDirectory( self.mergeSourceDir() ) )
            package.install()


        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        utils.debug( "Packagebase unmerge called", 2 )

        ## \todo mergeDestinationDir() reads the real used merge dir from the
        ## package definition, which fails if this is changed
        ## a better solution will be to save the merge sub dir into
        ## /etc/portage/installed and to read from it on unmerge
        utils.debug( "unmerge package from %s" % self.mergeDestinationDir(), 2 )
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            for prefix in [ "Release", "RelWithDebInfo", "Debug" ]:
                packageList = installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( prefix ) )
                for package in packageList:
                    fileList = package.getFiles()
                    utils.unmergeFileList( self.mergeDestinationDir(), fileList, self.forced )
                    package.uninstall()
        else:
            packageList = installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( ) )
            for package in packageList:
                fileList = package.getFiles()
                utils.unmergeFileList( self.mergeDestinationDir(), fileList, self.forced )
                package.uninstall()

        # only packages using a specific merge destination path are shared between build types
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( "Release" ) )
            installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( "RelWithDebInfo" ) )
            installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( "Debug" ) )
        else:
            installdb.getInstalledPackages( self.category, self.package, self._installedDBPrefix( ) )

        # run post-uninstall scripts
        if not emergeSettings.getboolean("General","EMERGE_NO_POST_INSTALL", False ):
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-uninstall-%s-%s.cmd" % ( self.package, pkgtype )
                script = os.path.join( self.mergeDestinationDir(), "manifest", scriptName )
                if os.path.exists( script ):
                    utils.debug("run post uninstall script '%s'" % script , 2)
                    cmd = "cd /D %s && %s" % ( self.mergeDestinationDir(), script )
                    if not utils.system(cmd):
                        utils.warning("%s failed!" % cmd )
                else:
                    utils.debug("post uninstall script '%s' not found" % script , 2)
        else:
            utils.debug("running of post uninstall scripts disabled!", 0)

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

        utils.debug( "PackageBase.execute called. args: %s" % sys.argv, 2 )
        command, _ = self.getAction(cmd)

        if self.subinfo.options.disableReleaseBuild and self.buildType() == "Release" \
                or self.subinfo.options.disableDebugBuild and self.buildType() == "Debug":
            print("target ignored for this build type")
            return False

        return self.runAction(command)

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
                     "package":        "createPackage",
                     "createpatch":    "createPatch",
                     "geturls":        "getUrls",
                     "print-revision":       "printSourceVersion",
                     "checkdigest":    "checkDigest",
                     "dumpdeps":       "dumpDependencies"}
        if command in functions:
            try:
                ok = getattr(self, functions[command])()
            except AttributeError as e:
                raise portage.PortageException( str( e ), self.category, self.package )

        else:
            ok = utils.error( "command %s not understood" % command )

        return ok
