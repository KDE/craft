# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

from EmergeBase import *;
import os;
import utils;
import emergePlatform;
from graphviz import *;
import dependencies;
from InstallDB import *;

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
        utils.debug("PackageBase.__init__ called",2)
        EmergeBase.__init__(self)
        self.subinfo.options.readFromEnv()
        self.setBuildTarget()
        self.forceCreateManifestFiles = False

    def __installedDBPrefix(self, buildType=None):
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
        if isDBEnabled():
            if self.isTargetBuild():
                if installdb.isInstalled( category=None, package=self.package, prefix=os.getenv( "EMERGE_TARGET_PLATFORM" ) ):
                    ignoreInstalled = True
                    self.unmerge()
            else:
                prefixPath=self.__installedDBPrefix( self.buildType() )
                if installdb.isInstalled( category=None, package=self.package, prefix=prefixPath ):
                    ignoreInstalled = True
                    self.unmerge()
        else:
            if portage.isInstalled( '', self.package, '', self.buildType() ):
                ignoreInstalled = True
                self.unmerge()

        self.manifest()

        utils.debug("qmerge package to %s" % self.mergeDestinationDir(),2)
        utils.mergeImageDirToRootDir( self.mergeSourceDir(), self.mergeDestinationDir() )

        # run post-install scripts
        if not os.getenv("EMERGE_NO_POST_INSTALL") == "True":
            for pkgtype in ['bin', 'lib', 'doc', 'src']:
                scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
                script = os.path.join( self.rootdir, "manifest", scriptName )
                if os.path.exists( script ):
                    cmd = "cd %s && %s" % ( self.rootdir, script )
                    utils.system( cmd ) or utils.warning("%s failed!" % cmd )
        else:
            utils.debug("running of post-install scripts disabled!", 0)

        # add package to installed database -> is this not the task of the manifest files ? 
       
        # only packages using a specific merge destination path are shared between build types 
        if self.useBuildTypeRelatedMergeRoot and self.subinfo.options.merge.ignoreBuildType \
                and self.subinfo.options.merge.destinationPath != None:
            for prefix in [ "Release", "RelWithDebInfo", "Debug" ]:
                if isDBEnabled():
                    package = installdb.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix( prefix ), ignoreInstalled )
                    package.addFiles( utils.getFileListFromManifest(  self.__installedDBPrefix( prefix ), self.package ) )
                    package.install()
                else:
                    portage.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix( prefix ) )
        else:
            if isDBEnabled():
                if emergePlatform.isCrossCompilingEnabled():
                    if self.isTargetBuild():
                        package = installdb.addInstalled( self.category, self.package, self.version, os.getenv( "EMERGE_TARGET_PLATFORM" ), ignoreInstalled )
                    else:
                        package = installdb.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
                    package.addFiles( utils.getFileListFromDirectory( self.mergeSourceDir() ) )
                    package.install()
                else:
                    package = installdb.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix(), ignoreInstalled )
                    package.addFiles( utils.getFileListFromDirectory( self.mergeSourceDir() ) )
                    package.install()
            else:
                portage.addInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )

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
                    packageList = installdb.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix( prefix ) )
                    for package in packageList:
                        fileList = package.getFiles()
                        utils.unmergeFileList( self.mergeDestinationDir(), fileList, self.forced )
                        package.uninstall()
            else:
                if self.isTargetBuild():
                    packageList = installdb.remInstalled( self.category, self.package, self.version, os.getenv( "EMERGE_TARGET_PLATFORM" ) )
                else:
                    packageList = installdb.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
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
            portage.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix( "Release" ) )
            portage.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix( "RelWithDebInfo" ) )
            portage.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix( "Debug" ) )
        else:
            portage.remInstalled( self.category, self.package, self.version, self.__installedDBPrefix() )
        return True

    def cleanImage( self ):
        """cleanup before install to imagedir"""
        if hasattr(self,'buildSystemType') and self.buildSystemType == 'binary' or hasattr(self,'buildsystem') and self.buildsystem.buildSystemType == 'binary':
            utils.debug("skipped cleaning image dir because we use binary build system",1)
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

    def cleanAllBuilds( self ):
        """cleanup all build directories"""
        if os.path.exists( self.buildRoot() ):
            utils.cleanDirectory( self.buildRoot() )
            utils.debug( "cleaning all build dirs: %s" % self.buildRoot(), 1 )

        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
    
        utils.debug("base manifest called",2)
        if not utils.hasManifestFile( self.mergeDestinationDir(), self.category, self.package ) or self.forceCreateManifestFiles:
            utils.debug("creating of manifest files triggered", 1)
            utils.createManifestFiles( self.mergeSourceDir(), self.mergeSourceDir(), self.category, self.package, self.version )
        return True

    def stripLibs( self, pkgName ):
        """strip debugging informations from shared libraries"""
        basepath = os.path.join( self.installDir() )
        dllpath = os.path.join( basepath, "bin", "%s.dll" % pkgName )

        cmd = "strip -s " + dllpath
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
        """called to run the derived class"""
        """this will be executed from the package if the package is started on its own"""
        """it shouldn't be called if the package is imported as a python module"""

        utils.debug( "EmergeBase.execute called. args: %s" % sys.argv, 2 )
        (command, option) = self.getAction(cmd)
                
        #if self.createCombinedPackage:
        #    oldBuildType = os.environ["EMERGE_BUILDTYPE"]                        
        #    os.environ["EMERGE_BUILDTYPE"] = "Release"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = "Debug"
        #    self.runAction(command)
        #    os.environ["EMERGE_BUILDTYPE"] = oldBuildType
        #else:
        if self.subinfo.options.disableReleaseBuild and self.buildType() == "Release" or self.subinfo.options.disableDebugBuild and self.buildType() == "Debug":
            print "target ignored for this build type"
            return False
        
        if emergePlatform.isCrossCompilingEnabled() and self.isHostBuild() and self.subinfo.disableHostBuild and not command == "fetch" and not command == "unpack":
            utils.debug( "host build disabled, skipping host build", 1 )
            return True
            
        if emergePlatform.isCrossCompilingEnabled() and self.isTargetBuild() and self.subinfo.disableTargetBuild and not command == "fetch" and not command == "unpack":
            utils.debug( "target build disabled, skipping target build", 1 )
            return True
        
        self.runAction(command)
        return True

    def runAction( self, command ):
        ok = True
        if command   == "fetch":       ok = self.fetch()
        elif command == "cleanimage":  ok = self.cleanImage()
        elif command == "cleanbuild":  ok = self.cleanBuild()
        elif command == "cleanallbuilds":  ok = self.cleanAllBuilds()
        elif command == "unpack":      ok = self.unpack()
        elif command == "compile":     ok = self.compile()
        elif command == "configure":   ok = self.configure()
        elif command == "make":        ok = self.make()
        elif command == "install":     ok = self.install()
        elif command == "test":        ok = self.unittest()
        elif command == "qmerge":      ok = self.qmerge()
        elif command == "unmerge":     ok = self.unmerge()
        elif command == "manifest":    ok = self.manifest()
        elif command == "package":     ok = self.createPackage()
        elif command == "createpatch": ok = self.createPatch()
        elif command == "printrev":    ok = self.sourceVersion()
        elif command == "checkdigest": ok = self.checkDigest()
        elif command == "dumpdeps":    ok = self.dumpDependencies()
        else:
            ok = utils.error( "command %s not understood" % command )

        if ( not ok ):
            utils.die( "command %s failed" % command )
        return True
        
    def dumpEmergeDependencies(self):
        """dump emerge package dependencies"""
        output = dependencies.dumpDependencies(self.package)
        outDir = self.buildDir()
        outFile = os.path.join(outDir,self.package+'-emerge.dot')
        f = open(outFile,"w")
        f.write(output);
        f.close()

        graphviz = GraphViz(self)

        if not graphviz.runDot(outFile, outFile+'.pdf', 'pdf'):
            return False

        return graphviz.openOutput()
        
        return True
                