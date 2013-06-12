# -*- coding: utf-8 -*-
import info
import os
from Package.QMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'
      self.hardDependencies[ 'kdesupport/qjson' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'svnHEAD' ] = 'https://quazip.svn.sourceforge.net/svnroot/quazip/trunk/quazip'
      self.patchToApply['svnHEAD'] = ('quazip-0.4.4.diff',1)
      self.targets['0.4.4'] = 'http://heanet.dl.sourceforge.net/project/quazip/quazip/0.4.4/quazip-0.4.4.zip'
      self.targetDigests['0.4.4'] = 'cfc5ca35ff157e77328fc55de40b73591f425592'
      self.targetInstSrc['0.4.4'] = 'quazip-0.4.4'
      self.patchToApply['0.4.4'] = ('quazip-0.4.4.diff',1)
      self.defaultTarget = '0.4.4'


class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
