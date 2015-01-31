import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/pixman.git'
        self.patchToApply['gitHEAD'] = [ ( "0001-add-cmake-build-system.patch", 1 ) ]
        self.shortDescription = "a library that provides low-level pixel manipulation features such as image compositing and trapezoid rasterization."
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

