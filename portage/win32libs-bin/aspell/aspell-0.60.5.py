# -*- coding: iso-8859-15 -*-
from Package.BinaryPackageBase import *
from Package.BinaryPackageBase import *        

import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.60.5-1']:
            self.targets[ version ] = repoUrl + """/aspell-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/aspell-""" + version + """-lib.tar.bz2"""

        self.targetDigests['0.60.5-1'] = ['49390a52915739ac8edd345a5fe2c54dfbd07ecd',
                                          '68cd4dc50d26f524965df8d792668af4f413ebd3']
        self.defaultTarget = '0.60.5-1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
