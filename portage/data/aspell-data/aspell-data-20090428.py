import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://winkde.org/pub/kde/ports/win32/repository/aspell"""
        
        self.targets[ '0.60' ] = repoUrl + """/aspell-en-6.0-41-bin.tar.bz2
                           """ + repoUrl + """/aspell-de-0.60.20030222.1-10-bin.tar.bz2"""

        self.defaultTarget = '0.60'
            
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
