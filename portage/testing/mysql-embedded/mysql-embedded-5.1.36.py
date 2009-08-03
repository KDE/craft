import info

# version 5.1.36 contains only debug libraries 

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['5.1.36-2'] = """
http://downloads.sourceforge.net/kde-windows/mysql-embedded-5.1.36-2-bin.tar.bz2
http://downloads.sourceforge.net/kde-windows/mysql-embedded-5.1.36-2-lib.tar.bz2
"""
        self.targetInstSrc['5.1.36-2'] = ""
        self.defaultTarget = '5.1.36-2'

    def setDependencies( self ):
        """ """
        self.hardDependencies['gnuwin32/wget'] = 'default'
        #self.hardDependencies['testing/mysql-server'] = 'default' 
        # the include files are used in the mysql-server package already
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
