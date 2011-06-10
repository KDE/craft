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

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'msys'
        self.subinfo.options.configure.defines = "--enable-shared=no --enable-ltdl-install"
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
     Package().execute()
