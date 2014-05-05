from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["0.21.1"] = "http://telepathy.freedesktop.org/releases/telepathy-glib/telepathy-glib-0.21.1.tar.gz"
        self.targetInstSrc["0.21.1"] = "telepathy-glib-0.21.1"
        self.defaultTarget = "0.21.1"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
        self.dependencies['testing/glib-src'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=yes --enable-shared=no --disable-modular-tests DBUS_LIBS='%s/lib/libdbus-1.dll.a' DBUS_CFLAGS=' '" % utils.toMSysPath(EmergeStandardDirs.emergeRoot())


        
