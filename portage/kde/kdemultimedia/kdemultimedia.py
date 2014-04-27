import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['gitHEAD'] = ''
        self.shortDescription = "KDE multimedia applications (jux, kmix, kmixctrl, kscd)"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        #self.dependencies['kde/audiocd-kio'] = 'default'#missing dep cdparanoia
        self.dependencies['kde/dragon'] = 'default'
        #self.dependencies['kde/ffmpegthumbs'] = 'default'
        self.dependencies['kde/juk'] = 'default'
        #self.dependencies['kde/kmix'] = 'default'#kmix on windows?
        #self.dependencies['kde/kscd'] = 'default'
        self.dependencies['kde/libkcddb'] = 'default'
        self.dependencies['kde/libkcompactdisc'] = 'default'
        self.dependencies['kde/mplayerthumbs'] = 'default'

#        self.dependencies['win32libs/taglib'] = 'default'
#        self.dependencies['win32libs/libogg'] = 'default'
#        self.dependencies['win32libs/libvorbis'] = 'default'

from Package.VirtualPackageBase import *

class Package(VirtualPackageBase):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

