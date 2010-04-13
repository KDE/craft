import os
import utils
import info
from Package.CMakePackageBase import *



class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.6.23.1'] = 'http://www.sqlite.org/sqlite-amalgamation-3.6.23.1.tar.gz'
        self.targetInstSrc['3.6.23.1'] = "sqlite-3.6.23.1"
        self.patchToApply['3.6.23.1'] = ( "sqlite-3.6.23.1-20100413.diff", 1 )
        self.defaultTarget = '3.6.23.1'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
