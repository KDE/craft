import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "gitHEAD" ] = "https://github.com/phacility/libphutil.git"
        self.defaultTarget = "gitHEAD"


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['binary/php'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils/arcanist/libphutil";

    def unpack(self):
        BinaryPackageBase.cleanImage()
        utils.copyDir(self.sourceDir(), self.imageDir())
        return True
    
