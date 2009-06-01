# -*- coding: utf-8 -*-
import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"

        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['0.18', '0.18.1']:
            self.targets[ ver ] = self.getPackage( repoUrl, "exiv2", ver )

        self.defaultTarget = '0.18.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
