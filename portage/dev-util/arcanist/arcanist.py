import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "gitHEAD" ] = "https://github.com/phacility/arcanist.git"
        self.defaultTarget = "gitHEAD"


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['binary/php'] = 'default'
        self.buildDependencies['dev-util/libphutil'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils/arcanist/arcanist"

    def unpack(self):
        BinaryPackageBase.cleanImage(self)
        utils.copyDir(self.sourceDir(), self.imageDir())
        arc_dir = os.path.join(EmergeStandardDirs.emergeRoot(), "dev-utils", "arcanist", "arcanist", "bin")
        utils.createBat(os.path.join(self.rootdir,"dev-utils","bin","arc.bat"), """
        set PATH=%s;%%PATH%%
        %s %%*""" % (arc_dir, os.path.join(arc_dir , "arc" )))
        return True

