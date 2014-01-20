import os
import sys
import info

# deprecated class
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'https://libface.svn.sourceforge.net/svnroot/libface/trunk'
        self.defaultTarget = 'svnHEAD'
        self.patchToApply['svnHEAD'] = ('libface-20120122.patch', 1)

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/opencv'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
