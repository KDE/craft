import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:skrooge'
        self.targets['0.9.1'] = "http://www.winkde.org/pub/kde/ports/win32/repository/other/skrooge-4c9e641.tar.bz2"
        self.targetInstSrc['0.9.1'] = "skrooge-4c9e641"
        self.patchToApply['0.9.1'] = ("skrooge-4c9e641-20110830.diff", 1)
        for ver in ['1.0.0', '1.1.1', '1.2.0', '1.6.0', '1.8.0']:
            self.targets[ ver ] = "http://skrooge.org/files/skrooge-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "skrooge-" + ver
        self.patchToApply['1.0.0'] = [("skrooge-1.0.0-20111009.diff", 1)]
        self.patchToApply['1.1.1'] = [("skrooge-1.1.1-20111208.diff", 1)]
        self.patchToApply['1.2.0'] = [("skrooge-1.2.0-20120114.diff", 1)]
        self.patchToApply['1.6.0'] = [("skrooge-1.6.0-20130307.diff", 1),
                                      ("0001-320226-Monthly-report-does-not-work-due-to-missing-t.patch", 1)]
        self.targetDigests['1.1.1'] = '063af1a04c2406babc59203e0d57912e834e46f1'
        self.targetDigests['1.2.0'] = '1587d493f6064637805e3601bdae08fd5258a633'
        self.shortDescription = "a personal finance manager for KDE"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs/libopensp'] = 'default'
        self.dependencies['win32libs/libofx'] = 'default'
        self.runtimeDependencies['kde/kde-runtime'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
