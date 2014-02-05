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
        #self.baseURL = "http://www.winkde.org/pub/kde/ports/win32/repository/other/"
        self.baseURL = "http://ftp.gwdg.de/pub/misc/mysql/Downloads/"
        for ver in [ '5.5.32' , '5.5.33' , '5.5.34', '5.6.14', '5.6.16' ]:
            ver2 = ver.split('.')
            url = self.baseURL + "MySQL-" + ver2[0] + "." + ver2[1] + "/"
            if( emergePlatform.buildArchitecture() == 'x64' ):
              self.targets[ ver ] = url+"mysql-" + ver + "-winx64.zip"
              self.targetInstSrc[ ver ] = "mysql-" + ver + "-winx64"
            else:
              self.targets[ ver ] = url+"mysql-" + ver + "-win32.zip"
              self.targetInstSrc[ ver ] = "mysql-" + ver + "-win32"
        if( emergePlatform.buildArchitecture() == 'x64' ):
              self.targetDigests['5.5.32'] = '9b6969ce7814ddb9fc9f7b39f0f59cc18ded98fc'
              self.targetDigests['5.5.33'] = 'eceac0d0a01e45feb11df26029913022351476e6'
              self.targetDigests['5.5.34'] = '32cb59f0c4cba0aee4703c7c3757cb36a499bd68'
              self.targetDigests['5.6.14'] = '85458d57aa5198da9925dd6971eced779c8366e6'
              self.targetDigests['5.6.16'] = '957dd35ed8c183a642f8fcd372368bff703aaba3'
        else:
              self.targetDigests['5.5.32'] = '3d84eccbf05d0ef8117c0f1c1fbf5df277adacb0'
              self.targetDigests['5.5.33'] = 'fdf6523699576fe818a63722a994710b8b52f171'
              self.targetDigests['5.5.34'] = '89beeab279d251630629c15d4ce8e29e84b8087d'
              self.targetDigests['5.6.14'] = '6d702c2f72555163bc5c49f857f8105790e6dfa5'
              self.targetDigests['5.6.16'] = '94fd04dbb92019757ada6c7ea73aa6db827019b4'

        self.shortDescription = "MySql database server and embedded library"
        self.defaultTarget = '5.6.16'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


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
