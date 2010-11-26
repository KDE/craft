# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdelibs'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdelibs'
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'svnHEAD'

    
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['virtual/kdelibs-base'] = 'default'
        self.dependencies['dev-util/perl'] = 'default'
        self.dependencies['dev-util/automoc'] = 'default'
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies['kdesupport/phonon'] = 'default'
        self.dependencies['kdesupport/attica'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['kdesupport/dbusmenu-qt'] = 'default'
            self.dependencies['kdesupport/qca'] = 'default'
            self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.dependencies['data/docbook-dtd'] = 'default'
        self.dependencies['data/docbook-xsl'] = 'default'
        self.dependencies['kdesupport/soprano'] = 'default'
        self.dependencies['kdesupport/strigi'] = 'default'
        self.dependencies['win32libs-bin/shared-desktop-ontologies'] = 'default'

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

        if emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += \
                    "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
        if self.isHostBuild():
            self.subinfo.options.configure.defines += "-DBUILD_kdoctools=TRUE "
        if self.isTargetBuild():
            self.subinfo.options.configure.defines += \
                    "-DKDE_PLATFORM_PROFILE=Mobile "\
                    "-DBUILD_kutils=TRUE "\
                    "-DBUILD_kross=TRUE "\
                    "-DBUILD_interfaces=TRUE "

if __name__ == '__main__':
    Package().execute()
