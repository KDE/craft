import base
import info

# needed from:
#        kdeedu

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['3.10', '3.14']:
            self.targets[ version ] = repoUrl + """/cfitsio-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/cfitsio-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '3.14'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
