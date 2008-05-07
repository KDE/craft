import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/workspace'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        for ver in ['70', '71', '72', '73']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-workspace-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdebase-workspace-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "workspace"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DBUILD_libs=OFF"
        self.kdeCustomDefines += " -DBUILD_systemsettings=OFF"
        self.kdeCustomDefines += " -DBUILD_kcheckpass=OFF"
        self.kdeCustomDefines += " -DBUILD_kscreensaver=OFF"
        self.kdeCustomDefines += " -DBUILD_solid=OFF"
        self.kdeCustomDefines += " -DBUILD_ksmserver=OFF"
        self.kdeCustomDefines += " -DBUILD_kcminit=OFF"
        self.kdeCustomDefines += " -DBUILD_ksplash=OFF"
        self.kdeCustomDefines += " -DBUILD_ksysguard=OFF"
        self.kdeCustomDefines += " -DBUILD_klipper=OFF"
        self.kdeCustomDefines += " -DBUILD_kmenuedit=OFF"
        self.kdeCustomDefines += " -DBUILD_krunner=OFF"
        self.kdeCustomDefines += " -DBUILD_kwin=OFF"
        self.kdeCustomDefines += " -DBUILD_plasma=OFF"
        self.kdeCustomDefines += " -DBUILD_printer-applet=OFF"
        self.kdeCustomDefines += " -DBUILD_kstartupconfig=OFF"
        self.kdeCustomDefines += " -DBUILD_khotkeys=OFF"
        self.kdeCustomDefines += " -DBUILD_kcontrol=OFF"
        self.kdeCustomDefines += " -DBUILD_ksystraycmd=OFF"
        self.kdeCustomDefines += " -DBUILD_doc=OFF"
#        self.kdeCustomDefines += " -DBUILD_wallpapers=OFF"
   
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebase-workspace", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebase-workspace", os.path.basename(sys.argv[0]).replace("kdebase-workspace-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
