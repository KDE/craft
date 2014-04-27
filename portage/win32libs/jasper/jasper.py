import os

import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.900.1-2' ] = 'http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip'
        self.targetInstSrc[ '1.900.1-2' ] = os.path.join( 'jasper-1.900.1', 'src', 'libjasper' )
        self.patchToApply[ '1.900.1-2' ] = ( "jasper-1.900.1-20130523.diff", 3 )
        self.shortDescription = "A library to manipulate JPEG-2000 images"
        self.defaultTarget = '1.900.1-2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/jpeg'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

