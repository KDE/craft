# -*- coding: utf-8 -*-
import base
import info

SRC_URI= """
http://winkde.org/pub/kde/ports/win32/repository/other/Git-1.6.3-preview20090507-2.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.3'] = SRC_URI
        self.targetInstSrc['1.6.3'] = ""
        self.defaultTarget = '1.6.3'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instdestdir = "dev-utils"
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
