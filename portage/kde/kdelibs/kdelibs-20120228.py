# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdelibs|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.9.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.9." + ver + "/src/kdelibs-4.9." + ver + ".tar.xz"
            self.targetInstSrc['4.9.' + ver] = 'kdelibs-4.9.' + ver
        self.patchToApply['4.9.0'] = [("kdelibs-4.9.0-20120219.diff", 1),
                                      ("kdecore-add-kdeconf.diff", 1),
                                      ("fix-plasma-crash.diff", 1)]
        self.patchToApply['4.9.4'] = [("0001-fixed-crash-for-unknow-property-added-icon-support-f.patch",1),
                                      ("0001-fixed-two-issues-and-implemented-basic-battery-suppo.patch",1)]
        self.shortDescription = "The KDE Library"
        self.defaultTarget = 'gitHEAD'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['win32libs-bin/automoc'] = 'default'
        self.dependencies['kdesupport/hupnp'] = 'default'
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies['kdesupport/phonon'] = 'default'
        self.dependencies['kdesupport/attica'] = 'default'
        self.dependencies['kdesupport/dbusmenu-qt'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.dependencies['kdesupport/soprano'] = 'default'
        self.dependencies['kdesupport/strigi'] = 'default'
        self.dependencies['virtual/kdelibs-base'] = 'default'
        self.dependencies['data/docbook-dtd'] = 'default'
        self.dependencies['data/docbook-xsl'] = 'default'
        self.dependencies['data/shared-desktop-ontologies'] = 'default'
        self.runtimeDependencies['kdesupport/phonon-vlc'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if compiler.isMinGW():
          self.subinfo.options.configure.defines += " -DKDE_DISTRIBUTION_TEXT=\"MinGW %s\" " % compiler.getMinGWVersion()
        elif compiler.isMSVC():
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"%s\" " % compiler.getVersion()

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        if compiler.isMinGW():
            manifest = os.path.join( self.packageDir(), "kconf_update.exe.manifest" )
            executable = os.path.join( self.installDir(), "bin", "kconf_update.exe" )
            utils.embedManifest( executable, manifest )
        return True

if __name__ == '__main__':
    Package().execute()
