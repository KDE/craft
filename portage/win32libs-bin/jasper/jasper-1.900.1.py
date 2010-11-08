from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.900.1-2']:
            self.targets[ version ] = repoUrl + """/jasper-""" + version + """-bin.zip
                                """ + repoUrl + """/jasper-""" + version + """-lib.zip"""

        self.targetDigests['1.900.1-2'] = ['23894fcf9840105ae6049d49aefaf5ebfe5ce6df',
                                           'b564176fc9a53a3afc626bcdc6ca2fd16a6bac44']
        self.defaultTarget = '1.900.1-2'

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
