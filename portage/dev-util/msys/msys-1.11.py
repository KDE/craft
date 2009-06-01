# -*- coding: utf-8 -*-
import base
import utils
from utils import die
import os
import info

SRC_URI = """
http://downloads.sourceforge.net/sourceforge/mingw/msysCORE-1.0.11-20080826.tar.gz
http://downloads.sourceforge.net/sourceforge/mingw/gettext-devel-0.16.1-MSYS-1.0.11-1.tar.bz2
http://downloads.sourceforge.net/sourceforge/mingw/gettext-0.16.1-MSYS-1.0.11-1.tar.bz2
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.11'] = SRC_URI
        self.defaultTarget = '1.11'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, SRC_URI, args=args )
        self.instdestdir = "msys"
        self.subinfo = subinfo()
	
if __name__ == '__main__':
    subclass().execute()
