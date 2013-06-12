# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.defaultTarget = '3.1.0'
        self.shortDescription = "an advanced digital photo management application"
        
        self.svnTargets['gitHEAD'] = '[git]kde:digikam-software-compilation'
        for ver in ['1.0.0', '1.1.0', '1.6.0', '1.7.0', '2.0.0', '2.1.1', '2.3.0', '2.4.1', '2.5.0', '2.6.0', '2.7.0', '2.8.0']:
            self.targets[ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/' + ver + '/digikam-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'digikam-' + ver
        for ver in ['2.9.0', '3.0.0', '3.1.0']:
            self.targets[ver] = 'http://download.kde.org/stable/digikam/digikam-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'digikam-' + ver
        for ver in ['3.0.0-beta1a', '3.0.0-beta2', '3.0.0-rc', '3.2.0-beta1', '3.2.0-beta2']:
            self.targets[ver] = 'http://download.kde.org/unstable/digikam/digikam-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'digikam-' + ver
        
        self.patchToApply['1.7.0'] = ('digikam-1.7.0-20101219.diff', 1)
        self.patchToApply['2.0.0'] = ('digikam-2.0.0-20110825.diff', 1)
        for ver in ['gitHEAD', '1.1.0', '2.6.0', '2.7.0', '3.0.0-beta1a', '3.0.0-rc', '3.0.0', '3.1.0', '3.2.0-beta1', '3.2.0-beta2']:
            self.patchToApply[ver] = ('digikam-' + ver + '.diff', 1)
    
    def setBuildOptions( self ):
        info.infoclass.setBuildOptions(self)
        
        self.options.configure.defines = "-DENABLE_INTERNALMYSQL=OFF"
        if self.buildTarget in ['1.0.0', '1.1.0', '1.6.0', '1.7.0', '2.0.0', '2.1.1', '2.3.0', '2.4.1', '2.5.0']:
            self.options.configure.defines += " -DENABLE_GPHOTO2=OFF"
            self.options.configure.defines += " -DENABLE_NEPOMUKSUPPORT=OFF"
            self.options.configure.defines += " -DDIGIKAMSC_USE_PRIVATE_KDEGRAPHICS:BOOL=1"
        elif self.buildTarget in ['2.6.0', '2.7.0', '2.8.0', '2.9.0', '3.0.0-beta1a', '3.0.0-beta2', '3.0.0-rc', '3.0.0', '3.1.0', '3.2.0-beta1', '3.2.0-beta2']:
            self.options.configure.defines += " -DENABLE_NEPOMUKSUPPORT=OFF"
            self.options.configure.defines += " -DENABLE_LCMS2=ON"
            self.options.configure.defines += " -DDIGIKAMSC_CHECKOUT_PO=OFF"
            self.options.configure.defines += " -DDIGIKAMSC_COMPILE_PO=ON"
            self.options.configure.defines += " -DDIGIKAMSC_COMPILE_DOC=ON"
            self.options.configure.defines += " -DDIGIKAMSC_USE_PRIVATE_KDEGRAPHICS=ON"
        elif self.buildTarget in ['gitHEAD']:
            self.options.configure.defines += " -DENABLE_NEPOMUKSUPPORT=OFF"
            self.options.configure.defines += " -DENABLE_LCMS2=ON"
            # set DIGIKAMSC_CHECKOUT_PO=ON (requires ruby) if you want to spend time pulling all the language source data (very slow)
            self.options.configure.defines += " -DDIGIKAMSC_CHECKOUT_PO=OFF"
            self.options.configure.defines += " -DDIGIKAMSC_COMPILE_PO=ON"
            self.options.configure.defines += " -DDIGIKAMSC_COMPILE_DOC=ON"
            self.options.configure.defines += " -DDIGIKAMSC_USE_PRIVATE_KDEGRAPHICS=ON"
            self.options.configure.defines += " -DKDE4_BUILD_TESTS=1"
    
    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.runtimeDependencies['kde/kde-workspace'] = 'default' #not explicitly required, but some components (such as theme support) require this
        if self.buildTarget in ['2.3.0', '2.4.1', '2.5.0', '2.6.0', '2.7.0', '2.8.0', '2.9.0', '3.0.0']:
            #glib is not explicitly required by digikam after 3.0.0, but may be required by dependencies
            self.dependencies['testing/glib-src'] = 'default' #this is optional and only required by a few components of digikam
        self.dependencies['win32libs/opencv'] = 'default'
        self.dependencies['kde/marble'] = 'default'
        #TODO: Currently using the git repositories directly by using the download-repos script from digikam-software-compilation, but should consider using individual portage files for each package
        #      especially since we would then have a separate file list for each component and could possibly write an installer that allows certain components to be turned on or off
        #self.dependencies['kde/libkdcraw'] = 'default'
        #self.dependencies['kde/libkexiv2'] = 'default'
        #self.dependencies['kde/libkipi'] = 'default'
        #self.dependencies['kdesupport/libkface'] = 'default'
        #self.dependencies['kdesupport/libkgeomap'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.buildDependencies['win32libs/boost-headers'] = 'default'
        if self.buildTarget in ['1.0.0', '1.1.0', '1.6.0', '1.7.0', '2.0.0', '2.1.1', '2.3.0', '2.5.0']:
            self.dependencies['win32libs/lcms'] = 'default'
        elif self.buildTarget in ['gitHEAD', '2.6.0', '2.7.0', '2.8.0', '2.9.0', '3.0.0-beta1a', '3.0.0-beta2', '3.0.0-rc', '3.0.0', '3.1.0', '3.2.0-beta1', '3.2.0-beta2']:
            self.dependencies['win32libs/lcms2'] = 'default'
        if self.buildTarget in ['gitHEAD', '3.0.0', '3.1.0', '3.2.0-beta1', '3.2.0-beta2']:
            self.dependencies['win32libs/lensfun'] = 'default'
            self.dependencies['kdesupport/kqoauth'] = 'kqoauth' # required by ImgurExport plug-in
            self.buildDependencies['dev-util/winflexbison'] = 'default' # required by panorama plug-in
        if self.buildTarget in ['gitHEAD', '3.1.0', '3.2.0-beta1', '3.2.0-beta2']:
            self.dependencies['testing/liblqr'] = 'default' # required by content aware resize feature
        if self.buildTarget in ['gitHEAD']:
            self.buildDependencies['dev-util/perl'] = 'default'


class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.make.supportsMultijob = False
    
    def fetch(self):
        if not CMakePackageBase.fetch(self):
            return False
        self.enterSourceDir()
        if self.subinfo.buildTarget == 'gitHEAD':
            utils.system( "perl.exe " + os.path.join( self.sourceDir(), "download-repos" ) )
        return True

if __name__ == '__main__':
    Package().execute()
