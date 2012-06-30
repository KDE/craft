from Package.CMakePackageBase import *
import info
import shutil
import os
import re
import urllib.request, urllib.parse, urllib.error
import emergePlatform

# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):
        #http://ftp.gwdg.de/pub/misc/mysql/Downloads/MySQL-5.5/mysql-5.5.24-win32.zip
        self.baseURL = "ftp://ftp.gwdg.de/pub/misc/mysql/Downloads/"
        if( emergePlatform.buildArchitecture() == 'x64' ):
          self.targets[ '5.1.63'] = self.baseURL+"MySQL-5.1/mysql-noinstall-5.1.63-winx64.zip"
          self.targetInstSrc[ '5.1.56' ] = "mysql-5.1.63-winx64"
          self.targets[ '5.5.24'] = self.baseURL+"MySQL-5.5/mysql-5.5.24-winx64.zip"
          self.targetInstSrc[ '5.5.24' ] = "mysql-5.5.24-winx64"
        else:
          self.targets[ '5.1.63'] = self.baseURL+"MySQL-5.1/mysql-noinstall-5.1.63-win32.zip"
          self.targetInstSrc[ '5.1.63' ] = "mysql-5.1.63-win32"          
          self.targetDigests['5.1.63'] = '37827259cb5319d91940ff4f825e23165364305d'
          self.targets[ '5.5.24'] = self.baseURL+"MySQL-5.5/mysql-5.5.24-win32.zip"
          self.targetInstSrc[ '5.5.24' ] = "mysql-5.5.24-win32"
        self.shortDescription = "MySql database server and embedded library"
        self.defaultTarget = '5.5.24'


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(CMakePackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.disableStriping = True
    CMakePackageBase.__init__( self )


  def compile( self ):
    return True

  def install( self ):
    if( not self.cleanImage()):
      return False
    if self.subinfo.buildTarget.startswith("5.1"):
        shutil.copytree( os.path.join( self.sourceDir() , "bin" ) , os.path.join( self.installDir(), "bin") , ignore=shutil.ignore_patterns('*.pdb','*.map','*test.exe','mysqld-debug.exe') )
        # do not create lib files, just take the given ones, because of the stdcall problem
        os.mkdir( os.path.join( self.installDir(), "lib"  ) )
        shutil.copy( os.path.join( self.sourceDir() , "lib" , "opt" , "libmysql.lib" ) , os.path.join( self.installDir(), "lib" , "libmysql.lib" ) )
        os.mkdir(os.path.join( self.installDir(), "lib" , "plugin"))
        shutil.copy( os.path.join( self.sourceDir() , "lib" , "plugin" , "ha_innodb_plugin.dll" ) , os.path.join( self.installDir(), "lib" , "plugin" , "ha_innodb_plugin.dll" ) )
        shutil.copy( os.path.join( self.sourceDir() , "Embedded" , "DLL" , "release" , "libmysqld.dll" ) , os.path.join( self.installDir(), "bin" , "libmysqld.dll" ) )
        shutil.copy( os.path.join( self.sourceDir() , "Embedded" , "DLL" , "release" , "libmysqld.lib" ) , os.path.join( self.installDir(), "lib" , "libmysqld.lib" ) )
        if compiler.isMinGW():
            utils.createImportLibs( "libmysqld" , self.installDir() )
            utils.createImportLibs( "libmysql" , self.installDir() )  
        shutil.copytree( os.path.join( self.sourceDir() , "include" ) , os.path.join( self.installDir(), "include" ) ,  ignore=shutil.ignore_patterns('*.def') )
        shutil.copytree( os.path.join( self.sourceDir() , "scripts" ) , os.path.join( self.installDir(), "scripts" ) )
        shutil.copytree( os.path.join( self.sourceDir() , "share" ) , os.path.join( self.installDir(), "share" ) , ignore=shutil.ignore_patterns('Makefile*') )
        shutil.copytree( os.path.join( self.sourceDir() , "data" ) , os.path.join( self.installDir(), "data" ) )
    else:
        shutil.copytree( os.path.join( self.sourceDir() , "bin" ) , os.path.join( self.installDir(), "bin") , ignore=shutil.ignore_patterns('*.pdb','*.map','*test*','mysqld-debug.exe','*.pl','debug*') )    
        shutil.copy( os.path.join( self.sourceDir() , "lib" , "libmysqld.dll" ) , os.path.join( self.installDir(), "bin" , "libmysqld.dll" ) )
        shutil.copy( os.path.join( self.sourceDir() , "lib" , "libmysql.dll" ) , os.path.join( self.installDir(), "bin" , "libmysql.dll" ) )
        shutil.copytree( os.path.join( self.sourceDir() , "lib" ) , os.path.join( self.installDir(), "lib") , ignore=shutil.ignore_patterns('*.pdb','*.map','debug*','libmysqld.dll','libmysql.dll','mysql*') ) 
        if compiler.isMinGW():
            utils.createImportLibs( "libmysqld" , self.installDir() )
            utils.createImportLibs( "libmysql" , self.installDir() )        
        shutil.copytree( os.path.join( self.sourceDir() , "include" ) , os.path.join( self.installDir(), "include" ) ,  ignore=shutil.ignore_patterns('*.def') )
        shutil.copytree( os.path.join( self.sourceDir() , "scripts" ) , os.path.join( self.installDir(), "scripts" ) )
        shutil.copytree( os.path.join( self.sourceDir() , "share" ) , os.path.join( self.installDir(), "share" ) , ignore=shutil.ignore_patterns('Makefile*') )
        shutil.copytree( os.path.join( self.sourceDir() , "data" ) , os.path.join( self.installDir(), "data" ) )
    return True

if __name__ == '__main__':
    Package().execute()
