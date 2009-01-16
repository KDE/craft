import base
import info

# needed from:
#        kdeedu

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['0.12.3']:
            self.targets[ version ] = repoUrl + """/libnova-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libnova-""" + version + """-lib.tar.bz2"""
            self.targetInstSrc[ version ] = 'libnova-' + version

        self.defaultTarget = '0.12.3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
