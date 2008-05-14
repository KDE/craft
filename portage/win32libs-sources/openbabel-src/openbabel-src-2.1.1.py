import base
import os
import shutil
import re
import utils
from utils import die
import info

PACKAGE_NAME         = "openbabel"
PACKAGE_VER          = "2.1.1"
PACKAGE_FULL_VER     = "2.1.1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )

SRC_URI= """
http://heanet.dl.sourceforge.net/sourceforge/openbabel/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

#
# this library is used by kdeedu/kalzium
# thanks to the people from Molekel (http://bioinformatics.org/molekel/wiki/Main/OpenBabel)
# for making most of it working and providing current instructions
#

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.1.1'] = 'http://heanet.dl.sourceforge.net/sourceforge/openbabel/openbabel-2.1.1.tar.gz'
        self.defaultTarget = '2.1.1'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, SRC_URI, args=args )
        self.instsrcdir = PACKAGE_FULL_NAME
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir , "openbabel-2.1.1-cmake.diff" ) )
        if utils.verbose() > 0:
            print cmd
        utils.system( cmd ) or die( "patchin'" )
        
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        # now do packaging with kdewin-packager
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
