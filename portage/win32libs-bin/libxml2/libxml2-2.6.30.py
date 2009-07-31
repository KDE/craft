from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.6.30-3']:
            self.targets[ version ] = repoUrl + """/libxml2-""" + version + """-bin.zip
                                """ + repoUrl + """/libxml2-""" + version + """-lib.zip"""

            
        self.defaultTarget = '2.6.30-3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
