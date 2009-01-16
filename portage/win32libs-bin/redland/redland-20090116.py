import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.0.3-5']:
            self.targets[ version ] = repoUrl + """/redland-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/redland-""" + version + """-lib.tar.bz2"""

            
        self.defaultTarget = '1.0.3-5'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
