import info
from Package.AntPackageBase import *

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://svn.apache.org/repos/asf/velocity/docbook/trunk'
        self.defaultTarget = 'svnHEAD'

class Package(AntPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AntPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
