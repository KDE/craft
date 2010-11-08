from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.6.30-3']:
            self.targets[ version ] = repoUrl + """/libxml2-""" + version + """-bin.zip
                                """ + repoUrl + """/libxml2-""" + version + """-lib.zip"""
        self.targetDigests['2.6.30-3'] = ['959bbc30337acc66dd30034c15a9be1bffcc9685',
                                          '5c273a8da82ad64d7c7ab6760e5424e57f3838dd']
            
        self.defaultTarget = '2.6.30-3'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        # 2.6.x needs iconv !
        #self.hardDependencies['win32libs-bin/win_iconv'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
