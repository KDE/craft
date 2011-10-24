#
# copyright (c) 2011 Patrick von Reth <patrick.vonreth@gmail.com>
#

import utils
from CollectionPackagerBase import *

class SevenZipPackager2List( PackagerLists ):
    """ dummy name for PackagerLists """

class SevenZipPackager2( CollectionPackagerBase ):
    """
Packager for portal 7zip archives
"""
    def __init__( self, whitelists=None, blacklists=None):
        CollectionPackagerBase.__init__( self, whitelists, blacklists )
        self.packagerExe = None
        fileName = "bin\\7za.exe"
        for directory in [".", "dev-utils", "release", "debug"]:
            path = os.path.join(self.rootdir, directory, fileName )
            if os.path.exists(path):
                self.packagerExe = path
                break
        if self.packagerExe:
            utils.debug("using 7za from %s" % self.packagerExe, 2)



    def generate7zipPackage( self ):
        """create 7z package with digest files located in the manifest subdir"""

        if not self.packagerExe:
            utils.die("could not find 7za in your path!")

        if self.package.endswith( "-package" ):
            shortPackage = self.package[ : -8 ]
            if shortPackage.endswith("-sevenzip"):
                shortPackage = shortPackage[:-9]
        else:
            shortPackage = self.package


        if not "setupname" in self.defines or not self.defines[ "setupname" ]:
            self.defines[ "setupname" ] = "%s-portable-%s.7z" % ( shortPackage, self.buildTarget )
        if not "srcdir" in self.defines or not self.defines[ "srcdir" ]:
            self.defines[ "srcdir" ] = self.imageDir()
        if self.scriptname:
            utils.copyFile(self.scriptname,os.path.join(self.defines[ "srcdir" ],os.path.split(self.scriptname)[1]))
            
        # make absolute path for output file
        if not os.path.isabs( self.defines[ "setupname" ] ):
            dstpath = self.packageDestinationDir()
            self.defines[ "setupname" ] = os.path.join( dstpath, self.defines[ "setupname" ] )

        utils.deleteFile(self.defines[ "setupname" ])
        cmd = "cd %s && %s a -r %s %s" % (self.defines[ "srcdir" ], self.packagerExe,self.defines[ "setupname" ], '*.*')
        if not utils.system(cmd):
            utils.die( "while packaging. cmd: %s" % cmd )

    def createPackage( self ):
        """ create a package """
        print "packaging using the SevenzipPackager"
        
        self.internalCreatePackage()

        self.generate7zipPackage()
        utils.createDigetFile( self.defines[ "setupname" ])
        return True
