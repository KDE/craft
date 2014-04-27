import os

import info
import compiler
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies( self ):
        if not utils.varAsBool(emergeSettings.get("General",'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES', "False")):
            self.buildDependencies['gnuwin32/wget']       = 'default'
            self.buildDependencies['dev-util/7zip']       = 'default'
            self.buildDependencies['gnuwin32/patch']      = 'default'
            self.buildDependencies['gnuwin32/sed']        = 'default'
            self.buildDependencies['dev-util/cmake']      = 'default'
            self.buildDependencies['dev-util/subversion'] = 'default'
            self.buildDependencies['dev-util/git']        = 'default'

        # for creating combined packages
        self.buildDependencies['dev-util/pexports']   = 'default'

        if not utils.varAsBool(emergeSettings.get("General",'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES', "False")):
            self.buildDependencies['dev-util/putty']      = 'default'

            if compiler.isMinGW():
                if compiler.isMinGW_WXX():
                    self.buildDependencies['dev-util/mingw-w64']    = 'default'
            if emergeSettings.get("General","EMERGE_MAKE_PROGRAM" ,"" ) != "":
                self.buildDependencies['dev-util/jom'] = 'default'
            if utils.varAsBool( emergeSettings.get("General","EMERGE_USE_NINJA", "False")):
                self.buildDependencies['dev-util/ninja'] = 'default'
            if utils.varAsBool( emergeSettings.get("General","EMERGE_USE_CCACHE","False")):
                self.buildDependencies['win32libs/ccache'] = 'default'


class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
