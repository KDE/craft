import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:pykde4'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['testing/sip'] = 'default'
        self.hardDependencies['testing/pyqt'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.destinationPath = "emerge/python"
        
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
