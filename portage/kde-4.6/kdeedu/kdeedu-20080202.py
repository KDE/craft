import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = ''
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['kde-4.6/libkdeedu'] = 'default'
        self.dependencies['kde-4.6/blinken'] = 'default'
        self.dependencies['kde-4.6/cantor'] = 'default'
        self.dependencies['kde-4.6/kalgebra'] = 'default'
        self.dependencies['kde-4.6/kalzium'] = 'default'
        self.dependencies['kde-4.6/kanagram'] = 'default'
        self.dependencies['kde-4.6/kbruch'] = 'default'
        self.dependencies['kde-4.6/kgeography'] = 'default'
        self.dependencies['kde-4.6/khangman'] = 'default'
        self.dependencies['kde-4.6/kig'] = 'default'
        self.dependencies['kde-4.6/kiten'] = 'default'
        self.dependencies['kde-4.6/klettres'] = 'default'
        self.dependencies['kde-4.6/kmplot'] = 'default'
        self.dependencies['kde-4.6/kstars'] = 'default'
        self.dependencies['kde-4.6/ktouch'] = 'default'
        self.dependencies['kde-4.6/kturtle'] = 'default'
        self.dependencies['kde-4.6/kwordquiz'] = 'default'
        self.dependencies['kde-4.6/marble'] = 'default'
        self.dependencies['kde-4.6/parley'] = 'default'
        self.dependencies['kde-4.6/rocs'] = 'default'
        self.dependencies['kde-4.6/step'] = 'default'

from Package.VirtualPackageBase import *

if __name__ == '__main__':
    Package(subinfo()).execute()
