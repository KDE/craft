from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):

        for version in [ '2.4.11' ]:
            repoUrl = 'http://downloads.sourceforge.net/kde-windows/openldap/' + version
            self.targets[ version ]          = self.getUnifiedPackage( repoUrl, 'openldap', version )
            self.targetDigestUrls[ version ] = self.getUnifiedPackage( repoUrl, 'openldap', version, '.tar.bz2.sha1' )

        self.defaultTarget = '2.4.11'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.withSources = False

if __name__ == '__main__':
    Package().execute()
