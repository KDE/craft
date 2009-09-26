from Package.BinaryPackageBase import *
import info

# needed from:
#        kdeedu

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['3.10', '3.14', '3.20']:
            self.targets[ version ] = repoUrl + """/cfitsio-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/cfitsio-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '3.20'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
