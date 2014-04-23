import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["0.8.0"] = "http://telepathy.freedesktop.org/releases/telepathy-logger/telepathy-logger-0.8.0.tar.bz2"
        self.targetInstSrc["0.8.0"] = "telepathy-logger-0.8.0"
        self.defaultTarget = "0.8.0"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=yes --enable-shared=no DBUS_LIBS='%s/lib/libdbus-1.dll.a' DBUS_CFLAGS=' '" % utils.toMSysPath(os.getenv("KDEROOT"))


        
if __name__ == '__main__':
    Package().execute()
