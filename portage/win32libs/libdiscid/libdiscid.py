import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.3.2'] = 'http://ftp.musicbrainz.org/pub/musicbrainz/libdiscid/libdiscid-0.3.2.tar.gz'
        self.targetInstSrc['0.3.2'] = 'libdiscid-0.3.2'
        self.targetDigests['0.3.2'] = '42293b6963c3652386dc6d928e8f69ce08bbee38'
        self.patchToApply['0.3.2'] = [("libdiscid-0.3.2-20130221.diff", 1)]
        self.shortDescription = "a C library for creating MusicBrainz DiscIDs from audio CDs"
        self.defaultTarget = '0.3.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
