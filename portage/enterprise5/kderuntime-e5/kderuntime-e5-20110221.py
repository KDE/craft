import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime'
        for version in ['4.4', '4.5', '4.6', '4.7', '4.8', '4.9']:
            self.svnTargets[version] = '[git]kde:kde-runtime|KDE/%s' % version
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdebase-runtime-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdebase-runtime-4.6.' + ver
        self.defaultTarget = '4.7'
        self.patchToApply['4.7'] = [('Revert-disable-nepomuk-runtime-on-Windows.patch', 1)]

        self.patchToApply['4.6.2'] = [('Not-only-use-hardcoded-install-path-on-Windows.patch', 1),
#                                      ('Revert-disable-nepomuk-runtime-on-Windows.patch', 1)
                                     ]
        self.patchToApply['4.6'] = self.patchToApply['4.6.2']
    def setDependencies( self ):
        self.dependencies['enterprise5/kdelibs-e5'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
#        self.dependencies['enterprise5/phonon-vlc-e5'] = 'default'
        self.dependencies['win32libs-sources/libssh-src'] = 'default'
        self.dependencies['win32libs-sources/libbfd-src'] = 'default'
        self.shortDescription = "KDE runtime libraries"

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        # Disable nepomukstrigifeeder autostart since there is no
        # use for it in the enterprise5 package and it otherwise
        # indexes and monitors the whole Users/ directory.
        confdir = os.path.join(self.installDir(), "share", "config")
        utils.createDir(confdir)
        with open(os.path.join(confdir, "nepomukserverrc"),"w") as f:
            f.write('[Service-nepomukstrigiservice]\n')
            f.write('autostart=false\n')
        return True

if __name__ == '__main__':
    Package().execute()
