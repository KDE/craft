# -*- coding: utf-8 -*-
import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "vc90"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"

        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['3.1.3']:
            self.targets[ version ] = repoUrl + """/libantlr-""" + compiler + """-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '3.1.3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
