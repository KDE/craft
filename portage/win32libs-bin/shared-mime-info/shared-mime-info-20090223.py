import base
import os
import info
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.51-1', '0.51-2', '0.60']:
            self.targets[ version ] = repoUrl + """/shared-mime-info-""" + version + """-bin.tar.bz2"""
        self.defaultTarget = '0.60'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.subinfo = subinfo()

  def install( self ):
    base.baseclass.install( self )
    print "self.compiler: " + self.compiler
    if self.compiler == "msvc2005":
      manifest = os.path.join( self.packagedir, "update-mime-database.exe.manifest" )
      manifest_dest = os.path.join( self.imagedir, "bin", "update-mime-database.exe.manifest" )
      patch = os.path.join( self.imagedir, "bin", "update-mime-database.exe" )
      shutil.copy( manifest, manifest_dest )
      cmd = "mt.exe -nologo -manifest %s -outputresource:%s;2" % ( manifest_dest, patch )
      utils.system( cmd )
    
    return True

if __name__ == '__main__':
    subclass().execute()
