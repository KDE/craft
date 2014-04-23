#
# copyright (c) 2012 Patrick von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules 

import shutil

from BuildSystem.QMakeBuildSystem import *


class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__( self ):
        QMakeBuildSystem.__init__(self)
        utils.putenv( "QMAKESPEC", os.path.join(os.getenv("KDEROOT"), 'mkspecs', self.platform ))
        

    def install( self, options=""):
       """implements the make step for Qt projects"""
       options += " INSTALL_ROOT=%s install" % self.imageDir()[2:]
       if not QMakeBuildSystem.install( self ,options):
           return False
           
       badPrefix = os.path.join(self.installDir(), os.getenv("KDEROOT")[3:])
       if os.getenv("KDEROOT")[3:] != "" and os.path.exists(badPrefix):
           for subdir in os.listdir(badPrefix):
               shutil.move(os.path.join(badPrefix, subdir), self.installDir())
           shutil.rmtree(badPrefix)

       if os.path.exists(os.path.join( self.installDir() , "bin" , "mkspecs") ):
            shutil.move( os.path.join( self.installDir() , "bin" , "mkspecs") , os.path.join( self.installDir(), "mkspecs" ) )
       return True



          

