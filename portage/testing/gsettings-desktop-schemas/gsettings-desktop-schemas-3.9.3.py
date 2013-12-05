from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["3.9.3"] = "http://ftp.gnome.org/pub/GNOME/sources/gsettings-desktop-schemas/3.9/gsettings-desktop-schemas-3.9.3.tar.xz"
        self.targetInstSrc["3.9.3"] = "gsettings-desktop-schemas-3.9.3"
        self.defaultTarget = "3.9.3"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.make.supportsMultijob = False
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=no --enable-shared=yes "


        
if __name__ == '__main__':
    Package().execute()
