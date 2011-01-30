import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/k3b'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['virtual/kdemultimedia'] = 'default'
        self.dependencies['win32libs-bin/libsamplerate'] = 'default'
        self.dependencies['testing/libdvdcss'] = 'default'
        #        self.dependencies['testing/libcdio'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
