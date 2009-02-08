import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.6.30-3']:
            self.targets[ version ] = repoUrl + """/libxml2-""" + version + """-bin.zip
                                """ + repoUrl + """/libxml2-""" + version + """-lib.zip"""

            
        self.defaultTarget = '2.6.30-3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
