# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = "http://www.winkde.org/pub/kde/ports/win32/repository/other"
        self.targets[ '4.3.2' ] = self.getPackage( repoUrl, "qt-static", '4.3.2', '.zip' )
        for version in ['4.5.1-1']:
            self.targets[ version ] = self.getPackage( repoUrl, "qt-static", version)
        self.defaultTarget = '4.5.1-1'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )
    self.subinfo.options.onlyReleaseBuilds = True
    self.subinfo.options.merge.destinationPath = "qt-static"

    def merge(self):
        """this package should not be merged into""" 
        return True

    def unmerge(self):
        """this package should not be unmerged into""" 
        return True

if __name__ == '__main__':
    Package().execute()
