import shutil
import os

from Package.BinaryPackageBase import *
import info


# currently only needed from kdenetwork


class subinfo(info.infoclass):
    def setTargets( self ):
        self.baseURL = "http://dev.mysql.com/get/Downloads/MySQL-5.6/"
        ver = '5.6.31'
        if compiler.isX64():
          self.targets[ ver ] = self.baseURL + "mysql-" + ver + "-winx64.zip"
          self.targetInstSrc[ ver ] = "mysql-" + ver + "-winx64"
        else:
          self.targets[ ver ] = self.baseURL + "mysql-" + ver + "-win32.zip"
          self.targetInstSrc[ ver ] = "mysql-" + ver + "-win32"
        if compiler.isX64():
              self.targetDigests[ver] = 'f5ac341ca3364d8fd53e38808bde976950111438'
        else:
              self.targetDigests[ver] = 'fcf126875ecf1d749d13cacd2faae50a82252b66'

        self.shortDescription = "MySql database server and embedded library"
        self.defaultTarget = ver


    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    BinaryPackageBase.__init__( self )
    self.subinfo.options.package.disableStriping = True
    self.subinfo.options.package.packSources = False


  def install( self ):
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

