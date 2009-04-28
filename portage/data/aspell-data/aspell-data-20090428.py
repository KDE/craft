import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://winkde.org/pub/kde/ports/win32/repository/aspell"""
        
        for version in ['0.60.20030222.1-10']:
            self.targets[ version ] = repoUrl + """/aspell-de-0.60.20030222.1-10-bin.tar.bz2"""

            
        self.defaultTarget = '0.60.20030222.1-10'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
