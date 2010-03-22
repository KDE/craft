# -*- coding: utf-8 -*-
import info
import utils
import subprocess

PACKAGE_CRAN_MIRROR     = 'http://ftp5.gwdg.de/pub/misc/cran'
PACKAGE_PATH            = '/bin/windows/base/'

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

    def setTargets( self ):
        self.targets['stable_latest'] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + 'R-release.exe'
        self.targets['devel'] = PACKAGE_CRAN_MIRROR + PACKAGE_PATH + 'R-devel.exe'
        self.defaultTarget = 'stable_latest'

from Package.BinaryPackageBase import *

# Installation approach based on expat-src-2.0.1.py.
# This basically just runs the upstream binary installer, then moves files to the KDE dir.
# Installation goes to dstdir/lib/R, since R comes with *a lot* of files in several subdirectories.
# This approach is also taken in the Debian packages, and probably other *n*x distributions.
# A convenience R.bat is added to dstdir/bin to have "R" in the path.
# Compiling R from source is possible, but terribly complex on Windows. See 
# http://cran.r-project.org/doc/manuals/R-admin.html#Installing-R-under-Windows for details.
#
# TODO:
#    - adding icons would really be nice (icons do get added on the build-machine, but not in the package)
#    - is there a way to run updatePackages() (in R) after an update? Do we even want this?
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        # don't use shortcut to unpack into imageDir()
        self.buildSystemType = 'custom'
        # create combined package
        self.subinfo.options.package.withCompiler = None

    def unpack( self ):
        # hopefully only one...
        for filename in self.localFileNames():
            self.system( os.path.join( self.downloadDir(), filename ) + " /DIR=\"" + self.workDir() + "\" /SILENT")
        return True

    def install( self ):
        srcdir = self.sourceDir()
        dstdir = self.installDir()

        utils.cleanDirectory( dstdir )
        os.makedirs (os.path.join (dstdir, "lib", "R"))
        os.makedirs (os.path.join (dstdir, "bin"))

        # place everything in dstdir/lib/R (similar to debian packaging)
        portage.remInstalled( self.category, self.package, "stablelatest" )
        utils.copyDir (srcdir, os.path.join (dstdir, "lib", "R"))

        # create a shortcut in dstdir/bin
        f = open(os.path.join (dstdir, "bin", "R.bat"), "w")
        f.write("REM redirect to R.exe, autocreated during installation\n" + os.path.join ("%~dsp0", "..", "lib", "R", "bin", "R.exe") + " %1 %2 %3 %4 %5 %6 %7 %8 %9\n")
        f.close()

        return True

    # Determine real version number by querying the installed R
    def getVersionFromR( self ):
        rcmd = os.path.join (self.installDir(), "lib", "R", "bin", "R.exe")
        if self.buildTarget == 'devel':
            version = subprocess.Popen([rcmd, '--no-save', '--slave', '-e', '"cat(paste(R.version$major,R.version$minor,sep=\'.\'),\'devel\',R.version$svn,sep=\'\')"'], stdout=subprocess.PIPE).communicate()[0]
        else:
            version = subprocess.Popen([rcmd, '--no-save', '--slave', '-e', '"cat(R.version$major,R.version$minor,sep=\'.\')"'], stdout=subprocess.PIPE).communicate()[0]
        return version

    def createPackage( self ):
        # HACK: assign to the magic var that appears to control the version naming
        self.subinfo.options.package.version = self.getVersionFromR()
        return BinaryPackageBase.createPackage(self)

if __name__ == '__main__':
    Package().execute()
