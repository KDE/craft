import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim|4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.7.' + ver + '/src/kdepim-4.7.' + ver + '.tar.bz2'
            self.targetInstSrc['4.7.' + ver] = 'kdepim-4.7.' + ver
        self.defaultTarget = 'gitHEAD'

        for target in self.targets:
            self.patchToApply[target] = [('disable-crypto-backend.patch', 1),
                        ('Add-kde4_app_icon-macro-for-mobile-targets.patch',1),
                        ('remove-old-icon-way.diff', 1),
                        ('broken-app-icons-fix.diff', 1)]

        self.patchToApply['4.7.0'] += [("kdepim-4.7.0-20110823.diff", 1)]

    def setDependencies( self ):
        self.runtimeDependencies['kde/kdepim-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        self.shortDescription = "KDE's Personal Information Management suite"
        

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "
        self.subinfo.options.configure.defines += " -DKDEPIM_MOBILE_UI=TRUE "

if __name__ == '__main__':
    Package().execute()
