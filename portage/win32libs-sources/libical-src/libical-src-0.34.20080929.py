import base
import utils
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'libical'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()
    
  def unpack( self ):
    print "libical unpack called for %s" % self.subinfo.buildTarget
    # do the svn fetch/update
    repo = 'https://freeassociation.svn.sourceforge.net/svnroot/freeassociation/trunk/'
    if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
        self.svnFetch( repo + self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
    else:
        return False
    utils.cleanDirectory( self.workdir )
    return True

  def compile( self ):
    if self.subinfo.buildTarget in self.subinfo.svnTargets.keys():
        self.kde.sourcePath = os.path.join( self.svndir, self.subinfo.svnTargets[ self.subinfo.buildTarget ] )
    else:
        return False
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    self.doPackaging( "libical", "0.34-0", True )

    return True

if __name__ == '__main__':
    subclass().execute()
