#
# copyright (c) 2012 Patrick von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules 

import os
import utils
import compiler
import shutil
import re

from BuildSystem.QMakeBuildSystem import *

class Qt5CoreBuildSystem(QMakeBuildSystem):
    def __init__( self ):
        QMakeBuildSystem.__init__(self)
        utils.putenv( "QMAKESPEC", os.path.join(os.getenv("KDEROOT"), 'mkspecs', self.platform ))
        os.putenv("INSTALL_ROOT",os.path.join(self.imageDir(),"bin"))

        
    def configure( self, configureDefines="" ):
        self.qt5LibnameWorkaround()
        return QMakeBuildSystem.configure(self,configureDefines)
          
    def qt5LibnameWorkaround(self):
        moduleDir =  os.path.join(self.sourceDir(),"modules")
        if not os.path.exists(moduleDir):
          moduleDir =  os.path.join(self.sourceDir(),"src","modules")
        if os.path.exists(moduleDir):
            pattern = re.compile("^(QT.* = Qt.*)+(?<!5)$")
            filePattern = re.compile(".*\.pri")
            for module in os.listdir(moduleDir):
                if filePattern.match(module):
                  f_in = open(os.path.join(moduleDir,module),"rt+")
                  in_lines = f_in.readlines()
                  out_lines = list()
                  f_in.close()                  
                  changed = False
                  for line in in_lines:
                      if pattern.match(line):
                          changed = True
                          line = line.strip() + "5\n"
                      out_lines.append(line)
                      
                  if changed:
                      f_out = open(os.path.join(moduleDir,module),"wt+")
                      f_out.writelines(out_lines)
                      f_out.close()


    def install( self, options=None ):
       """implements the make step for Qt projects"""
       if not QMakeBuildSystem.install( self ,options):
           return False
       if not  os.path.exists(os.path.join( self.installDir(), "bin" )):
          os.mkdir( os.path.join( self.installDir(), "bin" ) )

       if os.path.exists( os.path.join( self.installDir(), "lib" )): 
           for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
               if file.endswith( ".dll" ):
                   utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
       if os.path.exists(os.path.join( self.installDir() , "bin" , "mkspecs") ):
            shutil.move( os.path.join( self.installDir() , "bin" , "mkspecs") , os.path.join( self.installDir(), "mkspecs" ) )
       return True



          

