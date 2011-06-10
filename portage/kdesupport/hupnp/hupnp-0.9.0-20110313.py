# -*- coding: utf-8 -*-
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "https://hupnp.svn.sourceforge.net/svnroot/hupnp/trunk/herqq"
        self.shortDescription = "Herqq UPnP (HUPnP) is a software library for building UPnP devices and control points conforming to the UPnP Device Architecture version 1.1"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/libqtsoap'] = 'default'

    def setBuildOptions( self ):
        self.options.configure.defines = '-r "CONFIG += DISABLE_TESTAPP"'
        self.options.configure.defines = '-r "CONFIG += DISABLE_AVTESTAPP"'
        self.options.configure.defines += ' -r "CONFIG += DISABLE_QTSOAP"'

from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        if self.buildType() == "Release":
            self.subinfo.options.configure.defines += ' -r "CONFIG -= debug"'
            self.subinfo.options.configure.defines += ' -r "CONFIG += release"'
            self.subinfo.options.configure.defines += ' -r "CONFIG -= debug_and_release"'
        if self.buildType() == "Debug":
            self.subinfo.options.configure.defines += ' -r "CONFIG += debug"'
            self.subinfo.options.configure.defines += ' -r "CONFIG -= release"'
            self.subinfo.options.configure.defines += ' -r "CONFIG -= debug_and_release"'
        if self.buildType() == "RelWithDebInfo":
            self.subinfo.options.configure.defines += ' -r "CONFIG -= debug"'
            self.subinfo.options.configure.defines += ' -r "CONFIG -= release"'
            self.subinfo.options.configure.defines += ' -r "CONFIG += debug_and_release"'
        
    def unpack( self ):
        if not QMakePackageBase.unpack( self ):
            return False
        return True
        
    def install( self ):
        if not QMakePackageBase.install( self ):
            return False
        #sic.: the .lib file is placed under bin dir in hupnp
        utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "hupnp", "bin" ) , os.path.join( self.installDir(), "lib" ) )
        utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "hupnp", "include" ) , os.path.join( self.installDir(), "include" ) )
        utils.copySrcDirToDestDir( os.path.join( self.buildDir(), "hupnp", "deploy" ) , self.installDir() )
        os.mkdir( os.path.join( self.installDir(), "bin" ) )
        # copy over dlls as required by KDE convention
        for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
            if file.endswith( ".dll" ):
                utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
        return True
        
if __name__ == '__main__':
    Package().execute()
