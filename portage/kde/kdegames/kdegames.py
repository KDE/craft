import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'collection of computer games'

    def setDependencies( self ):
        self.dependencies['kde/bomber'] = 'default'
        self.dependencies['kde/bovo'] = 'default'
        self.dependencies['kde/granatier'] = 'default'
        self.dependencies['kde/kapman'] = 'default'
        self.dependencies['kde/katomic'] = 'default'
        self.dependencies['kde/knavalbattle'] = 'default'
        self.dependencies['kde/kblackbox'] = 'default'
        self.dependencies['kde/kblocks'] = 'default'
        self.dependencies['kde/kbounce'] = 'default'
        self.dependencies['kde/kbreakout'] = 'default'
        self.dependencies['kde/kdiamond'] = 'default'
        self.dependencies['kde/kfourinline'] = 'default'
        self.dependencies['kde/kgoldrunner'] = 'default'
        self.dependencies['kde/kigo'] = 'default'
        self.dependencies['kde/killbots'] = 'default'
        self.dependencies['kde/kiriki'] = 'default'
        self.dependencies['kde/kjumpingcube'] = 'default'
        self.dependencies['kde/klickety'] = 'default'
        self.dependencies['kde/klines'] = 'default'
        self.dependencies['kde/kmahjongg'] = 'default'
        self.dependencies['kde/kmines'] = 'default'
        self.dependencies['kde/knetwalk'] = 'default'
        self.dependencies['kde/kolf'] = 'default'
        self.dependencies['kde/kollision'] = 'default'
        self.dependencies['kde/konquest'] = 'default'
        self.dependencies['kde/kpat'] = 'default'
        self.dependencies['kde/kreversi'] = 'default'
        self.dependencies['kde/kshisen'] = 'default'
        self.dependencies['kde/ksirk'] = 'default'
        self.dependencies['kde/kspaceduel'] = 'default'
        self.dependencies['kde/ksquares'] = 'default'
        self.dependencies['kde/ksudoku'] = 'default'
        self.dependencies['kde/ksnakeduel'] = 'default'
        self.dependencies['kde/ktuberling'] = 'default'
        self.dependencies['kde/kubrick'] = 'default'
        self.dependencies['kde/libkdegames'] = 'default'
        self.dependencies['kde/lskat'] = 'default'
        self.dependencies['kde/palapeli'] = 'default'
        self.dependencies['kde/picmi'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

