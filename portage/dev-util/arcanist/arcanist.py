import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "master" ] = "https://github.com/phacility/arcanist.git"
        self.targetInstallPath[ "master" ] = "dev-utils/arcanist/arcanist"
        self.defaultTarget = "master"


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['binary/php'] = 'default'
        self.buildDependencies['dev-util/libphutil'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True

    def install( self ):
        if not BinaryPackageBase.install(self):
            return False
        arc_dir = os.path.join(CraftStandardDirs.craftRoot(), "dev-utils", "arcanist", "arcanist", "bin")
        utils.createBat(os.path.join(CraftStandardDirs.craftRoot(),"dev-utils","bin","arc.bat"), """
        set PATH=%s;%%PATH%%
        %s %%*""" % (arc_dir, os.path.join(arc_dir , "arc" )))
        return True

