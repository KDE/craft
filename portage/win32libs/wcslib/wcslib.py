import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        #self.targets['0.1'] = 'ftp://ftp.atnf.csiro.au/pub/software/wcslib/wcslib.tar.bz2'
        self.targets['0.1'] = 'http://raphaelcojocaru.xyz/wcslib515.tar.bz2'
		
        self.defaultTarget = '0.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'		

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DENABLE_STATIC=ON"