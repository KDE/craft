import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.900.1-2']:
            self.targets[ version ] = repoUrl + """/jasper-""" + version + """-bin.zip
                                """ + repoUrl + """/jasper-""" + version + """-lib.zip"""

            
        self.defaultTarget = '1.900.1-2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
