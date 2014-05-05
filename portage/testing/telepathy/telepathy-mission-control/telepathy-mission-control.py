from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["5.15.0"] = "http://telepathy.freedesktop.org/releases/telepathy-mission-control/telepathy-mission-control-5.15.0.tar.gz"
        self.targetInstSrc["5.15.0"] = "telepathy-mission-control-5.15.0"
        self.patchToApply["5.15.0"] = ("telepathy-mission-control-5.15.0-20130726.diff", 1)
        self.defaultTarget = "5.15.0"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=no --enable-shared=yes DBUS_LIBS='%s/lib/libdbus-1.dll.a' DBUS_CFLAGS=' '" % utils.toMSysPath(EmergeStandardDirs.emergeRoot())


        
