import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets["0.100.2"] = "http://krf.kollide.net/tmp/dbus-glib.tar.gz"
        self.targetInstSrc["0.100.2"] = "dbus-glib-0.100.2"
        self.patchToApply[ '0.100.2' ] = ("dbus-glib-0.100.2-20130713.diff",1)
        
        self.svnTargets["gitHEAD"] = "git://anongit.freedesktop.org/dbus/dbus-glib"
        self.defaultTarget = "0.100.2"
        

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'        
        self.buildDependencies['dev-util/pkg-config'] = 'default'
        self.dependencies['testing/glib-src'] = 'default'
            


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        if not self.subinfo.options.features.msys2:
            utils.die("Glib requries the msys2 feature activated to compile")
        self.subinfo.options.configure.defines = " --enable-gtk-doc=no --enable-static=yes --enable-shared=no --enable-tests=no DBUS_LIBS='%s/lib/libdbus-1.dll.a' DBUS_CFLAGS=' '" % utils.toMSysPath(emergeRoot())




