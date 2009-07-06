# -*- coding: utf-8 -*-

import os;
import utils;

from PackageBase import *;

from BuildSystem.BuildSystemFactory import *;
from Source.SourceFactory import *;
from Packager.PackagerFactory import *;

class PackageMultiBase (PackageBase):
    """Provides a generic interface for packages and implements the basic stuff for all packages"""
    
    buildSystemType = None
    packagerType = None
    
    def __init__(self):
        if utils.verbose > 1:
            print "PackageMultiBase.__init__ called"
        PackageBase.__init__(self)
        
    def execute(self):
        if utils.verbose > 1:
            print "PackageMultiBase.execute called"

        self.subinfo.setBuildTarget()
        # for conventience - todo is this really required 
        self.buildTarget = self.subinfo.buildTarget
            
        self.source = SourceFactory(self.subinfo)
        self.buildSystem = BuildSystemFactory(self.buildSystemType, self.source)
        self.packager = PackagerFactory(self.packagerType, self.buildSystem)
        
        PackageBase.execute(self)
                    
    def qmerge( self ):
        """mergeing the imagedirectory into the filesystem"""
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packagedir, "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
            if os.path.exists( script ):
                shutil.copyfile( script, destscript )
                             
        utils.mergeImageDirToRootDir( self.imageDir(), self.rootdir )

        # run post-install scripts
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, self.version, pkgtype )
            script = os.path.join( self.rootdir, "manifest", scriptName )
            if os.path.exists( script ):
                cmd = "cd %s && %s" % ( self.rootdir, script )
                utils.system( cmd ) or utils.warning("%s failed!" % cmd )
        utils.addInstalled( self.category, self.package, self.version )
        return True

    def unmerge( self ):
        """unmergeing the files from the filesystem"""
        if utils.verbose() > 1:
            print "base unmerge called"
        utils.unmerge( self.rootdir, self.package, self.forced )
        utils.remInstalled( self.category, self.package, self.version )
        return True

    def cleanup( self ):
        """cleanup before install to imagedir"""
        if ( os.path.exists( self.imageDir() ) ):
            utils.debug( "cleaning image dir: %s" % self.imageDir(), 1 )
            utils.cleanDirectory( self.imageDir() )
        return True
        
    def manifest( self ):
        """installer compatibility: make the manifest files that make up the installers"""
        """install database"""
        print "manifest should be created on qmerge "
    
        if utils.verbose() > 1:
            print "base manifest called"
        utils.manifestDir( os.path.join( self.workDir(), self.instsrcdir, self.package ), self.imagedir, self.category, self.package, self.version )
        return True

    def fetch(self):
        return self.source.fetch()
        
    def unpack(self):
        return self.source.unpack()

    def configure(self):
        return self.buildSystem.configure()

    def compile(self):
        return self.buildSystem.compile()

    def make(self):
        return self.buildSystem.make()

    def install(self):
        return self.buildSystem.install()
        
    def uninstall(self):
        return self.buildSystem.uninstall()

    def createPackage(self):
        return self.packageSystem.createPackage()

    def setDirectories(self):
        self.buildSystem.subinfo = self.subinfo
        #self.packageSystem.subinfo = self.subinfo
        return self.buildSystem.setDirectories()
    