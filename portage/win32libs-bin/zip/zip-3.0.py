from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/gnuwin32"""
        
        for version in ['2.31', '3.0']:
            self.targets[ version ] = repoUrl + """/zip-""" + version + """-bin.zip
                                """ + repoUrl + """/zip-""" + version + """-lib.zip
                                """ + repoUrl + """/zip-""" + version + """-dep.zip"""

            
        self.defaultTarget = '3.0'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
