# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.dependencies[ 'libs/qt' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'svnHEAD' ] = 'https://quazip.svn.sourceforge.net/svnroot/quazip/trunk/quazip'
      self.patchToApply['svnHEAD'] = ('quazip-20140331.patch',0)
      self.targets['0.4.4'] = 'http://heanet.dl.sourceforge.net/project/quazip/quazip/0.4.4/quazip-0.4.4.zip'
      self.targetDigests['0.4.4'] = 'cfc5ca35ff157e77328fc55de40b73591f425592'
      self.targetInstSrc['0.4.4'] = 'quazip-0.4.4'
      self.patchToApply['0.4.4'] = ('quazip-0.4.4.diff',1)
      self.defaultTarget = 'svnHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

