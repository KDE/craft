from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['20090813']:
            self.targets[ version ] = repoUrl + """/libssh-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libssh-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '20090813'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
