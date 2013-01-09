import os
import utils
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.5.35'] = 'http://switch.dl.sourceforge.net/project/flex/flex/flex-2.5.35/flex-2.5.35.tar.gz'
        self.targetDigests['2.5.35'] = '333c876a8e24ae5a17d9573459fc501b7721930b'
        self.patchToApply['2.5.35'] = ("flex-2.5.35-20120123.diff", 1)
        self.targetInstSrc['2.5.35'] = "flex-2.5.35"
        self.shortDescription = "something strange"
        self.defaultTarget = '2.5.35'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)


if __name__ == '__main__':
    Package().execute()
