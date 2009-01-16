import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"

        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['2.2.0']:
            self.targets[ version ] = repoUrl + """/openbabel-""" + compiler + """-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/openbabel-""" + compiler + """-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '2.2.0'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
