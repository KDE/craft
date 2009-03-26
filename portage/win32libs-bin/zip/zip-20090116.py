import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/gnuwin32"""
        
        for version in ['2.31']:
            self.targets[ version ] = repoUrl + """/zip-""" + version + """-bin.zip
                                """ + repoUrl + """/zip-""" + version + """-lib.zip
                                """ + repoUrl + """/zip-""" + version + """-dep.zip"""

            
        self.defaultTarget = '3.0'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
