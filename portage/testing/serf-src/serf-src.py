import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.7.2'] = 'http://serf.googlecode.com/files/serf-0.7.2.tar.bz2'
        self.targetInstSrc['0.7.2'] = 'serf-0.7.2'
        self.targetDigests['0.7.2'] = '132fbb13d50c4f849231eee79dcada8cde3ecad2'
        self.patchToApply['0.7.2'] = [("select-poll.patch", 0), ("serf-0.7.2-20110522.diff", 1)]
        self.defaultTarget = '0.7.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

