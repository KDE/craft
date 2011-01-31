import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim'
#        self.svnTargets['gitHEAD'] = '[git]kde:kdepim|4.6|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdepim-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdepim-4.6.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde-4.6/kdepim-runtime'] = 'default'
        self.dependencies['kde-4.6/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "
        self.subinfo.options.configure.defines += " -DKDEPIM_BUILD_MOBILE=FALSE "

if __name__ == '__main__':
    Package().execute()
