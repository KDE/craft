# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in [ '0.9.8j-1', '0.9.8k-3' ]:
            self.targets[ version ] = repoUrl + """/openssl-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/openssl-""" + version + """-lib.tar.bz2"""
        self.defaultTarget = '0.9.8k-3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
