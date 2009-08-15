import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.6.4'] = "http://subversion.tigris.org/files/documents/15/46471/svn-win32-1.6.4.zip"
        # this location affects class SvnSource 
        self.targetMergePath['1.6.4'] = "dev-utils/svn";
        self.targetMergeSourcePath['1.6.4'] = "svn-win32-1.6.4";
        self.defaultTarget = '1.6.4'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
   
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
