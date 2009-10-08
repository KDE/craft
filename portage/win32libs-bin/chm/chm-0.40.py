# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        elif os.getenv("KDECOMPILER") == "mingw4":
            compiler = "mingw4"
        elif os.getenv("KDECOMPILER") == "msvc2008":
            compiler = "vc90"

        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.40']:
            self.targets[ version ] = repoUrl + """/chm-""" + compiler + """-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '0.40'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
