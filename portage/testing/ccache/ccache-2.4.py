from Package.BinaryPackageBase import *
import info
import shutil
import os
import re
import urllib

# currently only needed from kdenetwork


class subinfo(info.infoclass):
  def setTargets( self ):    
    self.targets[ "ccache-win32-2.4" ]  =  "http://ccache-win32.googlecode.com/files/ccache-win32-2.4.zip"
    self.targetDigests['ccache-win32-2.4'] = 'b57ca0910f1fb4eb2d8b99974de71cb1018234f4'

    
    self.defaultTarget = "ccache-win32-2.4"
    

  def setDependencies( self ):
    self.hardDependencies['gnuwin32/wget'] = 'default'
    

class Package(BinaryPackageBase):
  def __init__(self):  
    self.subinfo = subinfo()    
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    BinaryPackageBase.__init__( self )
    self.subinfo.options.merge.destinationPath = "bin"
    
    
if __name__ == '__main__':
    Package().execute()
