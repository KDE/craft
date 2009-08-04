import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/workspace'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-workspace-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdebase-workspace-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
    
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        defines = ""
        defines += " -DBUILD_libs=OFF"
#        defines += " -DBUILD_systemsettings=OFF"
        defines += " -DBUILD_kcheckpass=OFF"
        defines += " -DBUILD_kscreensaver=OFF"
        defines += " -DBUILD_solid=OFF"
        defines += " -DBUILD_ksmserver=OFF"
        defines += " -DBUILD_kcminit=OFF"
        defines += " -DBUILD_ksplash=OFF"
        defines += " -DBUILD_ksysguard=OFF"
        defines += " -DBUILD_klipper=OFF"
        defines += " -DBUILD_kmenuedit=OFF"
#        defines += " -DBUILD_krunner=OFF"
        defines += " -DBUILD_kwin=OFF"
        defines += " -DBUILD_printer-applet=OFF"
        defines += " -DBUILD_kstartupconfig=OFF"
#        defines += " -DBUILD_khotkeys=OFF"
#        defines += " -DBUILD_kcontrol=OFF"
        defines += " -DBUILD_ksystraycmd=OFF"
#        defines += " -DBUILD_doc=OFF"
#        defines += " -DBUILD_plasma=OFF"
#        defines += " -DBUILD_wallpapers=OFF"
        self.subinfo.options.configure.defines = defines

if __name__ == '__main__':
    Package().execute()

