import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"

        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['7.8']:
            self.targets[ version ] = repoUrl + """/pcre-""" + compiler + """-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/pcre-""" + compiler + """-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '7.8'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
