# -*- coding: utf-8 -*-
import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['dbus4win-frank'] = 'http://www.kdab.net/~frank/dbus4win-20090527-3.zip'
        self.defaultTarget = 'dbus4win-frank'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.instsrcdir = os.path.join( "dbus4win-20090527-3", "cmake" )
    self.subinfo = subinfo()
    self.kdeCustomDefines = "-DDBUS_USE_EXPAT=ON -DDBUS_DISABLE_EXECUTABLE_DEBUG_POSTFIX=ON"

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
        return False

    print "dbus4win unpack called for %s" % self.subinfo.buildTarget

    if( not os.path.exists( self.workdir ) ):
        os.makedirs( self.workdir )

    return True

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    self.doPackaging( "dbus4win", self.buildTarget, False )

    return True

if __name__ == '__main__':
    subclass().execute()
