import base
import os
import utils
import info
import shutil

# this package is made from the official binaries by the following recipe(I am 
# currently to lazy to get this into a decent script):
# strip the package from the Docs, mysql-test, sql-bench directory
# throw away all the .exe files from the bin directory
# generate the mingw import libraries in the following way:
# reimp -d libmysqld.lib
# dlltool -k --input-def libmysqld.def --dllname libmysqld.dll --output-lib libmysqld.dll.a
# I used the release libraries for that, it might be possible to do this for the
# debug libraries too
# In the end I moved the content of Embedded\DLL\release to \bin and \lib
# respectively
# Patrick Spendrin <ps_ml@gmx.de>

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['5.1.28'] = """
http://winkde.org/pub/kde/ports/win32/repository/win32libs/mysql-embedded-5.1.28-1-bin.tar.bz2
http://winkde.org/pub/kde/ports/win32/repository/win32libs/mysql-embedded-5.1.28-1-lib.tar.bz2
"""
        self.targetInstSrc['5.1.28'] = ""
        self.defaultTarget = '5.1.28'

    def setDependencies( self ):
        """ """
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
