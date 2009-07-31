import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.1'] = "http://subversion.tigris.org/files/documents/15/45600/svn-win32-1.6.1.zip"
        # this location affects class SvnSource 
        self.targetMergePath['1.6.1'] = "dev-utils/svn";
        self.targetMergeSourcePath['1.6.1'] = "svn-win32-1.6.1";
        self.defaultTarget = '1.6.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
   
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
