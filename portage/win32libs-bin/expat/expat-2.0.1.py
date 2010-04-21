from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.0.1']:
            self.targets[ version ] = repoUrl + """/expat-""" + version + """-bin.zip
                                """ + repoUrl + """/expat-""" + version + """-lib.zip"""

        self.targetDigests['2.0.1'] = ['6c3cb5e87480003b42f19a45f6da27202732f137',
                                       '66799455180b0ddf66cd1da404948e5945b28139']            
        self.defaultTarget = '2.0.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
