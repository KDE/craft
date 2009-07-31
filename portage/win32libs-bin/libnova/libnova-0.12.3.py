from Package.BinaryPackageBase import *
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

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
