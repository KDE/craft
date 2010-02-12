# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# Packager base

from Packager.PackagerBase import *
import dump

class InnoSetupPackager (PackagerBase):
    """Packager for Inno Setup installations"""
    def __init__(self):
        PackagerBase.__init__(self)
        self.packagerExe = os.path.join(os.environ["ProgramFiles"],"Inno Setup 5","ISCC.exe")
        if self.packagerExe <> None:
            utils.debug("using inno setup packager from %s" % self.packagerExe,2)
            
    def configFile(self):
        """ return path of installer config file"""
        return os.path.join(self.packageDir(),"installer-config.iss")

    ## \todo rename to package()
    def createPackage(self):
        """packaging """
        print "createPackage from innosetupPackager"

        if not self.packagerExe:
            utils.die("could not find packager in your path!")

        if self.subinfo.options.package.packageName <> None:
            pkgName = self.subinfo.options.package.packageName
        else:
            pkgName = self.package
            
        if pkgName.endswith('-src'):
            pkgName = pkgName[:-4]

        if self.subinfo.options.package.version <> None:
            pkgVersion = self.subinfo.options.package.version
            pkgNotesVersion = pkgVersion
        elif self.subinfo.buildTarget == "gitHEAD" or self.subinfo.buildTarget == "svnHEAD":
            pkgVersion = str( datetime.date.today() ).replace('-', '')
            pkgNotesVersion = pkgVersion
        else: 
            pkgVersion = self.subinfo.buildTarget
            pkgNotesVersion = pkgVersion

        if "EMERGE_PKGPATCHLVL" in os.environ:
            pkgVersion += "-" + os.environ["EMERGE_PKGPATCHLVL"]

        if os.getenv("EMERGE_ARCHITECTURE") == "x64": 
            pkgName += "-x64"
        #else:
        #    pkgName += "-x86"
            
        # FIXME: add a test for the installer later
        dstpath = os.getenv( "EMERGE_PKGDSTDIR" )
        if not dstpath:
            dstpath = os.path.join( self.rootdir, "tmp" )
         
        for pkgtype in ['bin', 'lib', 'doc', 'src']:
            script = os.path.join( self.packageDir(), "post-install-%s.cmd" ) % pkgtype
            scriptName = "post-install-%s-%s-%s.cmd" % ( self.package, pkgVersion, pkgtype )
            destscript = os.path.join( self.imageDir(), "manifest", scriptName )
            if os.path.exists( script ):
                if not os.path.exists( os.path.join( self.imageDir(), "manifest" ) ):
                    os.mkdir( os.path.join( self.imageDir(), "manifest" ) )
                utils.copyFile( script, destscript )
        
        # determine source in case MultiSource is used
        if hasattr(self,'source'): 
            sourcedir = self.source.sourceDir()
        elif hasattr(self.parent,'source'): 
            sourcedir = self.parent.source.sourceDir()
        else:
            sourcedir = self.sourceDir()
        
        # todo: this is probably code for dealing with svn repositories 
        # need to be refactored
        if ( self.subinfo.options.package.packSources ):
            srcCmd = " -srcroot " + sourcedir
        else:
            srcCmd = ""

        if( self.subinfo.options.package.withCompiler ):
            if( self.compiler() == "mingw"):
              pkgName += "-mingw"
            elif self.compiler() == "mingw4":
              pkgName += "-mingw4"
            elif self.compiler() == "msvc2005":
              pkgName += "-msvc"
            elif self.compiler() == "msvc2008":
              pkgName += "-vc90"
            else:
              pkgName += "-unknown "

        cmd = "\"%s\" /O\"%s\" /F\"setup-%s-%s\"" % (self.packagerExe,self.buildRoot(),pkgName,pkgVersion)

        #
        # create config file from config File
        # 
        infile = self.configFile()
        _in = open(infile,'r')
        lines = _in.read().splitlines()
        _in.close()

        outfile = os.path.join(self.buildDir(),"temp.iss")
        out = open(outfile,'w')

        for line in lines:
            pattern = "@EMERGE_PACKAGE_VERSION@"
            a = line
            if a.find(pattern) > -1:
                a = line.replace(pattern,pkgVersion)
            pattern = "@EMERGE_INSTALL_DIR@"
            if a.find(pattern) > -1:
                a = line.replace(pattern,self.installDir())
            pattern = "@EMERGE_MERGE_DESTINATION_DIR@"
            if a.find(pattern) > -1:
                a = line.replace(pattern,self.mergeDestinationDir())
            out.write(a + "\n")
        out.close();

        cmd += " \"%s\"" % (outfile)
        utils.systemWithoutShell( cmd ) or utils.die( "while packaging. cmd: %s" % cmd )
        return True




