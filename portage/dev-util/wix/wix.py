import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        # requires nant, which is not supported yet
        #self.svnTargets['svnHEAD'] = '[hg]https://hg01.codeplex.com/wix|wix36'
        #self.defaultTarget = 'svnHEAD'
        
        # we only use the filename from the url for unpacking
        self.targets['3.5'] = "http://wix.codeplex.com/releases/acceptLicense/wix35-binaries.zip"
        self.targetDigests['3.5'] = '7e9bfd9935d9d61751dbf5163155cf75e8635f0d'
        self.defaultTarget = '3.5'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.unpack.unpackDir = "bin"
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"

    def fetch( self ):
        return self.system("wget -c -O %s\wix35-binaries.zip \"--post-data=fileId=204418&releaseId=60102&clickOncePath=\" http://wix.codeplex.com/releases/acceptLicense" % SourceBase.downloadDir())

