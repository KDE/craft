import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['6.b-5']:
            self.targets[ version ] = repoUrl + """/jpeg-""" + version + """-bin.zip
                                """ + repoUrl + """/jpeg-""" + version + """-lib.zip"""

            
        self.defaultTarget = '6.b-5'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
