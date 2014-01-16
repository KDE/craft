import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]kde:calligra"
        self.svnTargets['2.8'] = "[git]kde:calligra|calligra/2.8"
        
        for ver in ['2.7.90']:
            self.targets[ver] = "http://download.kde.org/unstable/calligra-" + ver + "/calligra-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = 'calligra-' + ver
        self.targetDigests['2.7.90'] = 'bc689b9644c0adfafa2cccd840a0abbdbf098ef8'
        self.patchToApply['2.7.90'] = [ ('patches/2.7.90/rng2cpp-fix.patch', 1),
                                        ('patches/2.7.90/deduplicate-includes-where-moc-fails-due-to-long-commandline.patch', 1),
                                        ('patches/2.7.90/gsl-cblas-link-fix.patch', 1),
                                        ('patches/2.7.90/disable-KoM2MMLFormulaTool-also-on-mingw.patch', 1),
                                        ('patches/2.7.90/fix-delete-array-operator.patch', 1),
                                        ('patches/2.7.90/fix-redefinitions-in-winquirks.patch', 1),
                                        ('patches/2.7.90/lst-to-list.patch', 1),
                                        ('patches/2.7.90/fix-isnan-usage.patch', 1),
                                        ('patches/2.7.90/fix-tests-linkage.patch', 1),
                                        ('patches/2.7.90/add-flags-to-vc-derived-macros-and-allow-multiple-definitions-on-mingw.patch', 1)]
        
        self.defaultTarget = '2.7.90'
        self.shortDescription = "The Calligra Suite of Applications"

    def setDependencies( self ):
        self.buildDependencies['kdesupport/eigen2'] = 'default'
        self.buildDependencies['win32libs/glew'] = 'default'
        self.buildDependencies['win32libs/boost-headers'] = 'default'
        self.dependencies['win32libs/lcms2'] = 'default'
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs/gsl'] = 'default'
        self.dependencies['win32libs/exiv2'] = 'default'
        self.dependencies['win32libs/openjpeg'] = 'default'
        self.dependencies['win32libs/icu'] = 'default'
        self.dependencies['win32libs/vc'] = 'default'
#        self.dependencies['win32libs/libfftw'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        defines = ""
        defines += "-DBUILD_doc=OFF "
        defines += "-DMEMORY_LEAK_TRACKER=OFF"

        self.subinfo.options.configure.defines = defines

if __name__ == '__main__':
    Package().execute()
