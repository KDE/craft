import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        compiler = "msvc"
        if os.getenv("KDECOMPILER") == "mingw":
            compiler = "mingw"
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.10.3', '0.10.4', '0.10.5']:
            self.targets[ version ] = repoUrl + """/poppler-"""+ compiler + """-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/poppler-"""+ compiler + """-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '0.10.5'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
