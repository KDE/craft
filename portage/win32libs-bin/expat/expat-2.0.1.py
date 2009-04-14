import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.0.1']:
            self.targets[ version ] = repoUrl + """/expat-""" + version + """-bin.zip
                                """ + repoUrl + """/expat-""" + version + """-lib.zip"""

            
        self.defaultTarget = '2.0.1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
