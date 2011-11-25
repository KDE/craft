import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepimlibs'

        self.targets['r1322'] = "http://saroengels.net/kde-windows/gnuwin32/gpgme-qt.tar.bz2"
        self.targetInstSrc['r1322'] = "gpgme-qt"
        #self.defaultTarget = 'r1322'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/gpgme'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/gpgme'] = 'default'
        else:
            self.dependencies['contributed/gpg4win-dev'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

        self.subinfo.options.configure.defines = "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

        if emergePlatform.isCrossCompilingEnabled():
            if self.isTargetBuild():
                self.subinfo.options.configure.defines += "-DKDEPIM_NO_KRESOURCES=ON -DMAILTRANSPORT_INPROCESS_SMTP=ON "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF -DKDEPIM_ONLY_KLEO=ON"

if __name__ == '__main__':
    Package().execute()
