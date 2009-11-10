import info

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['5.1.36-3'] = """
http://downloads.sourceforge.net/kde-windows/mysql-debug-5.1.36-3-bin.tar.bz2
"""
        self.targetInstSrc['5.1.36-3'] = ""
        self.defaultTarget = '5.1.36-3'

    def setDependencies( self ):
        """ """
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
