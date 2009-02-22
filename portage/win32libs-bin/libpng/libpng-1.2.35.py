import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.2.34', '1.2.35']:
            self.targets[ version ] = repoUrl + """/libpng-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libpng-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '1.2.35'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
