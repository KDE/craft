from Package.BinaryPackageBase import *
import info

# currently only needed from kdenetwork

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.9', '1.12', '1.13', '1.14', '1.15']:
            self.targets[ version ] = repoUrl + """/libidn-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libidn-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '1.15'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
