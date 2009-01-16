import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['4.1.4-1']:
            self.targets[ version ] = repoUrl + """/giflib-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/giflib-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '4.1.4-1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
