# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
       self.targets[ '0.18' ] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.tar.gz'
       self.targetInstSrc[ '0.18' ] = "gettext-0.18"
       self.patchToApply['0.18'] = [("gettext-0.18-20130523.diff", 1)]
       self.targetDigests['0.18'] = 'de396ec6877a451427d8597197d18c2d4b8f1a26'
       self.shortDescription = "GNU internationalization (i18n)"
       self.defaultTarget = '0.18'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/win_iconv'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
