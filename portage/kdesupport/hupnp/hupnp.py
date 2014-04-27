# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):        
        self.shortDescription = "Herqq UPnP (HUPnP) is a software library for building UPnP devices and control points conforming to the UPnP Device Architecture version 1.1"
        self.svnTargets['svnHEAD'] = "https://hupnp.svn.sourceforge.net/svnroot/hupnp/trunk/herqq"
        self.patchToApply['svnHEAD'] = ("HUpnp1.diff", 0)
        for ver in ["1.0.0"]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/hupnp/herqq-%s.zip" % ver
            self.targetInstSrc[ver] = "herqq-%s" % ver
        self.targetDigests['1.0.0'] = '543a67802c37c66c29c8527522b1630c42756545'
        
        self.defaultTarget = "1.0.0"

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/libqtsoap'] = 'default'


from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        QMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ' "PREFIX = %s" ' % self.imageDir().replace("\\","/")
        self.subinfo.options.configure.defines += ' "CONFIG += DISABLE_TESTAPP"'
        self.subinfo.options.configure.defines += ' "CONFIG += DISABLE_AVTESTAPP"'
        self.subinfo.options.configure.defines += ' "CONFIG += DISABLE_QTSOAP"'
        self.subinfo.options.configure.defines += ' "CONFIG += rtti"'
        
    def install( self ):
        if not QMakePackageBase.install( self ):
            return False
        #sic.: the .lib file is placed under bin dir in hupnp)
        os.mkdir( os.path.join( self.installDir(), "bin" ) )
        # copy over dlls as required by KDE convention
        for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
            if file.endswith( ".dll" ):
                utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
        return True
        

        
