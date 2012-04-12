# -*- coding: utf-8 -*-
import compiler
import info
import portage
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtdeclarative.git" 

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['libs/qtscript'] ='default'


from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        os.putenv("INSTALL_ROOT",os.path.join(self.imageDir(),"bin"))

        
    def install( self ):
        if not QMakePackageBase.install( self ):
            return False
        #sic.: the .lib file is placed under bin dir in hupnp)
        os.mkdir( os.path.join( self.installDir(), "bin" ) )
        # copy over dlls as required by KDE convention
        for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
            if file.endswith( ".dll" ):
                utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
        shutil.move( os.path.join( self.installDir() , "bin" , "mkspecs") , os.path.join( self.installDir(), "mkspecs" ) )
        return True
        

        
if __name__ == '__main__':
    Package().execute()
