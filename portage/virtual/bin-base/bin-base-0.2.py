import info
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies( self ):
        if not os.getenv('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            self.buildDependencies['gnuwin32/wget'] = 'default'
            self.buildDependencies['gnuwin32/patch'] = 'default'
            if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'
                self.buildDependencies['dev-util/perl'] = 'default'
                self.buildDependencies['dev-util/autotools'] = 'default'

from Package.VirtualPackageBase import *
from Source.SourceBase import *

class Package(VirtualPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
