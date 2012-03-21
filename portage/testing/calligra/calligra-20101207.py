import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]kde:calligra"
        self.svnTargets['gitStable'] = "[git]kde:calligra|calligra/2.4|"
        for ver in ['2.3.92']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/unstable/calligra-' + ver + '/calligra-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'calligra-' + ver
        self.targetDigests['2.3.92'] = '460d01bbb454140e851f7ea251d3ac8e143215e5'
        self.patchToApply['2.3.92'] = [ ("0001-INCLUDE-CheckFunctionExists-before-using-check_funct.patch", 1),
                                        ("0001-make-it-possible-to-find-openjpeg-on-windows.patch", 1),
                                        ("0002-For-pure-C-programs-MSVC-requires-that-variables-mus.patch", 1)
                                      ]
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/lcms2'] = 'default'
        self.dependencies['win32libs-bin/libwpd'] = 'default'
        self.dependencies['win32libs-bin/libwpg'] = 'default'
        self.dependencies['win32libs-bin/openjpeg'] = 'default'
        self.dependencies['win32libs-bin/libfftw'] = 'default'
        self.dependencies['win32libs-bin/glew'] = 'default'
        self.dependencies['virtual/kdepimlibs'] = 'default'
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['kdesupport/eigen2'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['kde/okular'] = 'default'
        self.dependencies['kde/libkdcraw'] = 'default'
        self.dependencies['testing/gsl'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
