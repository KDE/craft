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

        self.targetDigests['3.0'] = ['58ae2b1f3e19811a1888f155c98297f763a4c5e7',
                                     '81a004049348ab458cfcb4c4bdd2e42bf970fd4b',
                                     '1326746e38470a04e58fa2146d3455b81265e0d8']            
        self.defaultTarget = '3.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )
    self.subinfo.options.merge.destinationPath = 'dev-utils'

if __name__ == '__main__':
    Package().execute()
