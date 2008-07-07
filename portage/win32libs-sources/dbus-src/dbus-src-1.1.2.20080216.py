import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.1.2'] = 'tags/1.1.2'
        self.targetInstSrc['1.1.2'] = os.path.join( "dbus", "cmake" )
        self.svnTargets['svnHEAD'] = 'trunk'
        self.targetInstSrc['svnHEAD'] = os.path.join( "dbus", "cmake" )
        self.defaultTarget = 'svnHEAD'  # currently 1.2.1
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
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
    self.doPackaging( "dbus", "1.2.1-2", False )

    return True

if __name__ == '__main__':
    subclass().execute()
