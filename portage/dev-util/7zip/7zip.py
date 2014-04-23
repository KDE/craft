import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '916' , '920']:
            self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/sevenzip/7za%s.zip" % ver
            self.targetInstallPath[ ver ] = "bin"
        self.targetDigests[ '916' ] = 'b389a6e2f93c18daae20393532af0e4e85ebe6f4'
        self.targetDigests[ '920' ] = '9ce9ce89ebc070fea5d679936f21f9dde25faae0'
        self.defaultTarget = '920'


    def setDependencies( self ):
        self.buildDependencies[ 'gnuwin32/wget' ]       = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
