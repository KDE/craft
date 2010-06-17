from Package.BinaryPackageBase import *
import info
import shutil
import os
import utils

# currently only needed from kdenetwork


class subinfo(info.infoclass):
  def setTargets( self ):    
    self.targets[ "ccache-3.0pre1" ]  =  "http://ramiro.arrozcru.org/ccache-win32-1.exe"

    
    self.defaultTarget = "ccache-3.0pre1"
    

  def setDependencies( self ):
    self.hardDependencies['gnuwin32/wget'] = 'default'
    

class Package(BinaryPackageBase):
  def __init__(self):  
    self.subinfo = subinfo()    
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    BinaryPackageBase.__init__( self )

  def install(self):
    shutil.move(os.path.join( self.installDir() , "ccache-win32-1.exe") , os.path.join( self.installDir() , "bin" , "ccache.exe") )
    return True
    
if __name__ == '__main__':
    Package().execute()
