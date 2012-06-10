import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime|KDE/4.8|'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/kde-runtime-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'kde-runtime-4.8.0'
        for ver in ['1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/kde-runtime-4.8." + ver + ".tar.xz"
            self.targetInstSrc['4.8.' + ver] = 'kde-runtime-4.8.' + ver
        self.patchToApply['4.8.0'] = [("reenable-nepomuk-on-kde-runtime.diff", 1)]
        self.patchToApply['4.8.1'] = [("kde-runtime-4.8.1-20120319.diff", 1)]
        self.patchToApply['4.8.2'] = [("kde-runtime-4.8.1-20120319.diff", 1)]
        self.patchToApply['4.8.3'] = [("kde-runtime-4.8.1-20120319.diff", 1)]
        self.patchToApply['4.8.4'] = [("kde-runtime-4.8.1-20120319.diff", 1)]
        self.shortDescription = "Plugins and applications necessary for the running of KDE applications"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['win32libs-bin/libssh'] = 'default'
        if compiler.isMinGW_WXX():
            self.dependencies['win32libs-bin/libbfd'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
