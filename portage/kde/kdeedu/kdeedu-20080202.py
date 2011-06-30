import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/libkdeedu'] = 'default'
        self.dependencies['kde/blinken'] = 'default'
        self.dependencies['kde/cantor'] = 'default'
        self.dependencies['kde/kalgebra'] = 'default'
        self.dependencies['kde/kalzium'] = 'default'
        self.dependencies['kde/kanagram'] = 'default'
        self.dependencies['kde/kbruch'] = 'default'
        self.dependencies['kde/kgeography'] = 'default'
        self.dependencies['kde/khangman'] = 'default'
        self.dependencies['kde/kig'] = 'default'
        self.dependencies['kde/kiten'] = 'default'
        self.dependencies['kde/klettres'] = 'default'
        self.dependencies['kde/kmplot'] = 'default'
        self.dependencies['kde/kstars'] = 'default'
        self.dependencies['kde/ktouch'] = 'default'
        self.dependencies['kde/kturtle'] = 'default'
        self.dependencies['kde/kwordquiz'] = 'default'
        self.dependencies['kde/marble'] = 'default'
        self.dependencies['kde/parley'] = 'default'
        self.dependencies['kde/rocs'] = 'default'
        self.dependencies['kde/step'] = 'default'

from Package.VirtualPackageBase import *

if __name__ == '__main__':
    Package(subinfo()).execute()
