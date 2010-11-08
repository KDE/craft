from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['4.2.4']:
            self.targets[ version ] = repoUrl + """/libgmp-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libgmp-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '4.2.4'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
