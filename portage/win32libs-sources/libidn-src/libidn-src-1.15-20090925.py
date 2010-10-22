import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.19'
        self.targets[ ver ]       = 'ftp://ftp.gnu.org/gnu/libidn/libidn-%s.tar.gz' % ver
        self.targetDigests[ ver ] = '2b6dcb500e8135a9444a250d7df76f545915f25f'
        self.targetInstSrc[ ver ] = 'libidn-%s' % ver
        self.patchToApply[ ver ] = ("libidn-1.19-20101022.diff", 1)
        self.defaultTarget = ver

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def createPackage( self ): 

        self.stripLibs( "libidn-11" )
        self.createImportLibs( "libidn-11" )

        # now do packaging with kdewin-packager
        return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
     Package().execute()
