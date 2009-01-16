import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.31']:
            self.targets[ version ] = repoUrl + """/zip-""" + version + """-bin.zip
                                """ + repoUrl + """/zip-""" + version + """-lib.zip"""

            
        self.defaultTarget = '2.31'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
