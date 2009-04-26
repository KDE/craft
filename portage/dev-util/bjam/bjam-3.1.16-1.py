# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

PACKAGE_NAME         = "boost-jam"
PACKAGE_VER          = "3.1.16"
PACKAGE_FULL_VER     = "3.1.16-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER)

SRC_URI= """
http://downloads.sourceforge.net/boost/""" + PACKAGE_FULL_NAME + """-ntx86.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.1.16-1'] = SRC_URI
        self.targetInstSrc['3.1.16-1'] = PACKAGE_FULL_NAME + "-ntx86"
        self.defaultTarget = '3.1.16-1'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instdestdir = "dev-utils"
        self.subinfo = subinfo()

    def install( self ):
        if( not os.path.exists( os.path.join( self.imagedir, self.instdestdir, "bin" ) ) ):
            os.makedirs( os.path.join( self.imagedir, self.instdestdir, "bin" ) )

        src = os.path.join( self.workdir, self.instsrcdir, "bjam.exe" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "bjam.exe" )
        shutil.copy( src, dst )
        return True

    def make_package( self ):
        return self.doPackaging( PACKAGE_NAME, PACKAGE_VER, True )

if __name__ == '__main__':
    subclass().execute()
