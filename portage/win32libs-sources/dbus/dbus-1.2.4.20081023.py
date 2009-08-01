# -*- coding: utf-8 -*-
import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.1.2'] = 'tags/1.1.2'
        self.svnTargets['1.2.1'] = 'tags/1.2.1'
        self.svnTargets['1.2.3'] = 'tags/1.2.3'
        self.svnTargets['1.2.4'] = 'tags/1.2.4'
        self.svnTargets['svnHEAD'] = 'trunk'
        self.defaultTarget = '1.2.4'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.instsrcdir = os.path.join( "dbus", "cmake" )
    self.subinfo = subinfo()
    
  def unpack( self ):
    print "dbus unpack called for %s" % self.subinfo.buildTarget
    # do the svn fetch/update
    repo = 'https://windbus.svn.sourceforge.net/svnroot/windbus/'
    if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
        if( self.subinfo.buildTarget != 'svnHEAD' ):
            self.svndir += '/tags'
        self.svnFetch( repo + self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
    else:
        return False

    if self.buildTarget == '1.1.2':
      utils.cleanDirectory( self.workdir )
  
      # now copy the tree below destdir/trunk to workdir
      srcdir = self.svndir
      destdir = os.path.join( self.workdir, "dbus" )
      utils.copySrcDirToDestDir( srcdir, destdir )
  
      os.chdir( destdir )
      os.system( "patch -p0 < DBus-win32.patch" )
  
      #copy the needed changed cmake files over...
      destdir = os.path.join( self.workdir, "dbus", "cmake", "modules" )
      utils.copySrcDirToDestDir( self.filesdir, destdir )
  
      file = r"cmake\CMakeLists.txt"
      os.rename( file, "%s.orig" % file )
  
      # disable doc subdir in recent dbus svn
      sedcommand = r""" "s/add_subdirectory( doc )/###add_subdirectory( doc )/" """
  
      command = "type %s.orig | sed -e %s > %s" % ( file, sedcommand, file )
      #print "command:", command
      os.system( command )

    if( not os.path.exists( self.workdir ) ):
        os.makedirs( self.workdir )

    return True

  def compile( self ):
    if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
        self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ], "cmake" )
    else:
        return False
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
    self.doPackaging( "dbus", "1.2.4-1", True )

    return True

if __name__ == '__main__':
    subclass().execute()
