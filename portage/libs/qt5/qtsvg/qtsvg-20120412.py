# -*- coding: utf-8 -*-
import compiler
import info
import portage
import shutil


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.svnTargets['gitHEAD'] = "[git]git://gitorious.org/qt/qtsvg.git" 

        self.defaultTarget = "gitHEAD"

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        os.putenv("INSTALL_ROOT",os.path.join(self.imageDir(),"bin"))

    def configure(self):
        #cache = open(os.path.join( portage.getPackageInstance('libs','qtbase').buildDir() , ".qmake.cache" ), "rt+" )
        #text = cache.read()
        #cache.close()
        #text.replace("QMAKE_EXTRA_MODULE_FORWARDS .*","QMAKE_EXTRA_MODULE_FORWARDS = \"%s\"" % os.path.join( self.sourceDir() , "module-paths" ,"modules" ).replace("\\","/"))
        #cache = open(os.path.join(self.buildDir() , ".qmake.cache" ), "wt+" ) 
        #cache.write(text)
        #cache.close()
        return QMakePackageBase.configure( self )
        
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
