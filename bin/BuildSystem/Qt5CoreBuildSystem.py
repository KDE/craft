#
# copyright (c) 2012 Patrick von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules 

import os
import utils
import compiler
import shutil

from BuildSystem.QMakeBuildSystem import *

class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__( self ):
        QMakeBuildSystem.__init__(self)
        utils.putenv( "QMAKESPEC", os.path.join(os.getenv("KDEROOT"), 'mkspecs', self.platform ))
        os.putenv("INSTALL_ROOT",os.path.join(self.imageDir(),"bin"))



    def install( self, options=None ):
       """implements the make step for Qt projects"""
       if not QMakeBuildSystem.install( self ):
           return False
       if not  os.path.exists(os.path.join( self.installDir(), "bin" )):
          os.mkdir( os.path.join( self.installDir(), "bin" ) )
       for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
           if file.endswith( ".dll" ):
               utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
       shutil.move( os.path.join( self.installDir() , "bin" , "mkspecs") , os.path.join( self.installDir(), "mkspecs" ) )
       return True



          

