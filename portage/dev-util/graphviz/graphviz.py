import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.26.3'] = 'http://www.graphviz.org/pub/graphviz/stable/windows/graphviz-2.26.3.msi'
        self.targetDigests['2.26.3'] = '0ce70fcd7ce880ee19ecce6ef8e943d48a1a5374'
        self.defaultTarget = '2.26.3'

from Package.SetupPackageBase import *

class Package(SetupPackageBase):
    def __init__( self):
        SetupPackageBase.__init__(self)

