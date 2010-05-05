from Package.CMakePackageBase import *
import info
import shutil
import os
import re
import urllib
import platform

# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):   
        self.baseURL = "http://artfiles.org/mysql/Downloads/MySQL-5.1/"
        if( platform.buildArchitecture() == 'x64' ):
          self.targets[ 'mysql-sever-5.1.46'] = self.baseURL+"mysql-noinstall-5.1.46-winx64.zip"
          self.targetInstSrc[ 'mysql-sever-5.1.46' ] = "mysql-5.1.46-winx64"
          self.targetDigests[ 'mysql-sever-5.1.46' ] = 'eafb5d40ae09e8f208151c934089e6dd1ded98b4'
        else:
          self.targets[ 'mysql-sever-5.1.46'] = self.baseURL+"mysql-noinstall-5.1.46-win32.zip"
          self.targetInstSrc[ 'mysql-sever-5.1.46' ] = "mysql-5.1.46-winx32"
          self.targetDigests[ 'mysql-sever-5.1.46' ] = 'd1149263a9fc02ab4a1067a10e0eb7df35708290'
          
        self.defaultTarget = 'mysql-sever-5.1.46'
       

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
        
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
    shutil.copytree( os.path.join( self.sourceDir() , "bin" ) , os.path.join( self.installDir(), "bin") , ignore=shutil.ignore_patterns('*.pdb','*.map','*test.exe','mysqld-debug.exe') )
    shutil.copy( os.path.join( self.sourceDir() , "Embedded" , "DLL" , "release" , "libmysqld.dll" ) , os.path.join( self.installDir(), "bin" , "libmysqld.dll" ) )
    shutil.copytree( os.path.join( self.sourceDir() , "include" ) , os.path.join( self.installDir(), "include" ) ,  ignore=shutil.ignore_patterns('*.def') )
    shutil.copytree( os.path.join( self.sourceDir() , "scripts" ) , os.path.join( self.installDir(), "scripts" ) )
    shutil.copytree( os.path.join( self.sourceDir() , "share" ) , os.path.join( self.installDir(), "share" ) , ignore=shutil.ignore_patterns('Makefile*') )
    shutil.copytree( os.path.join( self.sourceDir() , "data" ) , os.path.join( self.installDir(), "data" ) )
    self.createImportLibs( "libmysql")
    self.createImportLibs( "libmysqld")
    return True 
    
if __name__ == '__main__':
    Package().execute()
