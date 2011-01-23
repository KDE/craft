# -*- coding: utf-8 -*-
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "https://hupnp.svn.sourceforge.net/svnroot/hupnp/trunk/herqq"
        self.patchToApply['svnHEAD'] = ("hupnp-0.8.0-20110122.diff", 1)
        self.shortDescription = "Herqq UPnP (HUPnP) is a software library for building UPnP devices and control points conforming to the UPnP Device Architecture version 1.1"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['kdesupport/libqtsoap'] = 'default'

from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        self.source.noCopy = False
        
    def unpack( self ):
        if not QMakePackageBase.unpack( self ):
            return False
            
        cache_content = ""
        cache_content += "CONFIG -= debug_and_release\n"
        # by now using release only
        # if self.buildType() == "Debug":
        #     cache_content += "CONFIG -= release\n"
        #     cache_content += "CONFIG += debug\n"
        # else:
        #     cache_content += "CONFIG += release\n"
        #     cache_content += "CONFIG -= debug\n"
        cache_content += "CONFIG += release\n"
        cache_content += "CONFIG -= debug\n"

        # write the .qmake.cache as it is done by the configure.bat
        cachefile = open( os.path.join( self.buildDir(), ".qmake.cache" ), "w+" )
        cachefile.write(cache_content)
        cachefile2 = open( os.path.join( self.buildDir(), "hupnp", "src", "hupnp_core", ".qmake.cache" ), "w+" )
        cachefile.write(cache_content)
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
