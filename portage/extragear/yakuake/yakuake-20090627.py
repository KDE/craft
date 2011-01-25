import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/yakuake'
        self.shortDescription = "a drop-down terminal emulator based on KDE Konsole technology"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kdebase-apps'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
