from Package.BinaryPackageBase import *
import info

# currently only needed from kdenetwork

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.7.2']:
            self.targets[ version ] = repoUrl + """/libgpod-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libgpod-""" + version + """-lib.tar.bz2"""

        self.defaultTarget = '0.7.2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['testing/glib'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
