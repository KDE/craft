from Package.CMakePackageBase import *
import info
import shutil
import os
import re
import urllib
import emergePlatform

# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):   
        arch = 'win32'
        if emergePlatform.buildArchitecture() == 'x64':
          arch = 'win64'
        self.targets[ '20100330' ] =  'http://downloads.sourceforge.net/project/virtuoso/virtuoso/6.1.1/vos6-' + arch + '-20100330.zip'
        self.targetInstSrc[ '20100330' ] = "virtuoso-opensource"
          
        self.defaultTarget = '20100330'
       

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        
        
class Package(CMakePackageBase):
  def __init__(self):  
    self.subinfo = subinfo()    
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None
    CMakePackageBase.__init__( self )
    
    
  def compile( self ):
    return True
    
  def install( self ):    
    if( not self.cleanImage()):
      return False
    
    shutil.copytree( self.sourceDir() , self.installDir(),ignore=shutil.ignore_patterns('libexpat.dll' ))
    
    return True 
    
if __name__ == '__main__':
    Package().execute()
