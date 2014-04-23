import info
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.2'] = ""
        self.defaultTarget = '0.2'

    def setDependencies( self ):
        if not utils.envAsBool('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            self.buildDependencies['gnuwin32/wget']       = 'default'
            self.buildDependencies['dev-util/7zip']       = 'default'
            self.buildDependencies['gnuwin32/patch']      = 'default'
            self.buildDependencies['gnuwin32/sed']        = 'default'
            self.buildDependencies['dev-util/cmake']      = 'default'
            self.buildDependencies['dev-util/subversion'] = 'default'
            self.buildDependencies['dev-util/git']        = 'default'

        # for creating combined packages
        self.buildDependencies['dev-util/pexports']   = 'default'

        if not utils.envAsBool('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES'):
            if os.getenv( "SVN_SSH" ) == "plink" or \
                    os.getenv( "GIT_SSH" ) == "plink":
                self.buildDependencies['dev-util/putty']      = 'default'

            if compiler.isMinGW():
                if compiler.isMinGW_WXX():
                    self.buildDependencies['dev-util/mingw-w64']    = 'default'
            if os.getenv( "EMERGE_MAKE_PROGRAM" ) != "":
                self.buildDependencies['dev-util/jom'] = 'default'
            if utils.envAsBool("EMERGE_USE_NINJA"):
                self.buildDependencies['dev-util/ninja'] = 'default'
            if utils.envAsBool("EMERGE_USE_CCACHE"):
                self.buildDependencies['win32libs/ccache'] = 'default'


class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
