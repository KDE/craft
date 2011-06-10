import os
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '2.2.8' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'libtool', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'libtool', version, '.tar.bz2.sha1' )

        self.defaultTarget = '2.2.8'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'msys'


if __name__ == '__main__':
     Package().execute()
