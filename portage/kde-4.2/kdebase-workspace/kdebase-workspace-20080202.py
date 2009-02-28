import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdebase/workspace'
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdebase-workspace-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdebase-workspace-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdelibs'] = 'default'
        self.hardDependencies['kde-4.2/kdepimlibs'] = 'default'
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "workspace"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DBUILD_libs=OFF"
#        self.kdeCustomDefines += " -DBUILD_systemsettings=OFF"
        self.kdeCustomDefines += " -DBUILD_kcheckpass=OFF"
        self.kdeCustomDefines += " -DBUILD_kscreensaver=OFF"
        self.kdeCustomDefines += " -DBUILD_solid=OFF"
        self.kdeCustomDefines += " -DBUILD_ksmserver=OFF"
        self.kdeCustomDefines += " -DBUILD_kcminit=OFF"
        self.kdeCustomDefines += " -DBUILD_ksplash=OFF"
        self.kdeCustomDefines += " -DBUILD_ksysguard=OFF"
        self.kdeCustomDefines += " -DBUILD_klipper=OFF"
        self.kdeCustomDefines += " -DBUILD_kmenuedit=OFF"
#        self.kdeCustomDefines += " -DBUILD_krunner=OFF"
        self.kdeCustomDefines += " -DBUILD_kwin=OFF"
        self.kdeCustomDefines += " -DBUILD_printer-applet=OFF"
        self.kdeCustomDefines += " -DBUILD_kstartupconfig=OFF"
#        self.kdeCustomDefines += " -DBUILD_khotkeys=OFF"
#        self.kdeCustomDefines += " -DBUILD_kcontrol=OFF"
        self.kdeCustomDefines += " -DBUILD_ksystraycmd=OFF"
#        self.kdeCustomDefines += " -DBUILD_plasma=OFF"
#        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_wallpapers=OFF"
   
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase-workspace", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
