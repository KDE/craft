# -*- coding: iso-8859-15 -*-
import base
import info

PACKAGE_NAME         = "Git"
PACKAGE_VER          = "1.6.2.2"
PACKAGE_FULL_VER     = "1.6.2.2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER)

SRC_URI= """
http://winkde.org/pub/kde/ports/win32/repository/other/"""  + PACKAGE_FULL_NAME + """.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.2.2'] = SRC_URI
        self.targetInstSrc['1.6.2.2'] = PACKAGE_FULL_NAME
        self.defaultTarget = '1.6.2.2'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instdestdir = "dev-utils"
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
