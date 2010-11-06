# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdelibs'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdelibs'
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdelibs'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdelibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdelibs-4.0.' + ver
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'svnHEAD'

    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['virtual/kdelibs-base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/attica'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.hardDependencies['kdesupport/dbusmenu-qt'] = 'default'
            self.hardDependencies['kdesupport/qca'] = 'default'
            self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['data/docbook-dtd'] = 'default'
        self.hardDependencies['data/docbook-xsl'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['win32libs-sources/shared-desktop-ontologies-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if self.compiler() == "mingw":
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW 3.4.5\" "
        elif self.compiler() == "mingw4":
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW 4.4.0\" "
        elif self.compiler() == "msvc2005":
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "
        elif self.compiler() == "msvc2008":
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2008 SP1\" "
        elif self.compiler() == "msvc2010":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2010\" "
          
        qmake = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        if not os.path.exists(qmake):
            utils.warning("could not find qmake in <%s>" % qmake)
        ## \todo a standardized way to check if a package is installed in the image dir would be good.
        self.subinfo.options.configure.defines += " -DQT_QMAKE_EXECUTABLE:FILEPATH=%s " \
            % qmake.replace('\\', '/')

        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")
            
        if self.isTargetBuild():
            self.subinfo.options.configure.defines += \
                    "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
            self.subinfo.options.configure.defines += \
                    "-DKDE_PLATFORM_PROFILE=Mobile "\
                    "-DBUILD_kutils=TRUE "\
                    "-DBUILD_kross=TRUE "\
                    "-DBUILD_interfaces=TRUE "

if __name__ == '__main__':
    Package().execute()
