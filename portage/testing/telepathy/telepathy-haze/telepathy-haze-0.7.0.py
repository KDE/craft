from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["0.7.0"] = "http://telepathy.freedesktop.org/releases/telepathy-haze/telepathy-haze-0.7.0.tar.gz"
        self.targetInstSrc["0.7.0"] = "telepathy-haze-0.7.0"
        self.defaultTarget = "0.7.0"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.make.supportsMultijob = False
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=no --enable-shared=yes DBUS_LIBS='%s/lib/libdbus-1.dll.a' DBUS_CFLAGS=' '" % utils.toMSysPath(os.getenv("KDEROOT"))


        
if __name__ == '__main__':
    Package().execute()
