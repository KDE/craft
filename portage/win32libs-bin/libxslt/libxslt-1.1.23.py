from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.1.23-3']:
            self.targets[ version ] = repoUrl + """/libxslt-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libxslt-""" + version + """-lib.tar.bz2"""

        self.targetDigests['1.1.23-3'] = ['15940112e47bd1fd4433dcdcd62ae9a2687c321a',
                                          'cf787d1d33187abc69e2e705b206657316843d49']
        self.defaultTarget = '1.1.23-3'

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
