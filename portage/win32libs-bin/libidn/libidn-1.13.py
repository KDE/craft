import base
import info

# currently only needed from kdenetwork

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.9', '1.12', '1.13']:
            self.targets[ version ] = repoUrl + """/libidn-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libidn-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '1.13'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
