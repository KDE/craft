import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['3.8.2-2']:
            self.targets[ version ] = repoUrl + """/tiff-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/tiff-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '3.8.2-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
