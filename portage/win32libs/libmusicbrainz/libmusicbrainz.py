import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['5.0.1'] = 'https://github.com/downloads/metabrainz/libmusicbrainz/libmusicbrainz-5.0.1.tar.gz'
        self.targetInstSrc['5.0.1'] = 'libmusicbrainz-5.0.1'
        self.targetDigests['5.0.1'] = 'd4823beeca3faf114756370dc7dd6e3cd01d7e4f'
        self.patchToApply['5.0.1'] = [("support-out-of-source-builds.diff", 1), ("libmusicbrainz-windows.diff", 1)]
        self.shortDescription = "a library for MusicBrainz lookup capabilities"
        self.defaultTarget = '5.0.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'        
        self.dependencies['win32libs/neon'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

