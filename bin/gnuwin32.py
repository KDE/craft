import base
import utils
import os

class gnuwin32class(base.baseclass):
  def __init__( self, SRC_URI ):
    base.baseclass.__init__( self, SRC_URI )

  def install( self ):
    if utils.verbose() > 1:
        print "gnuwin32 install called"
    destdir = self.imagedir
    utils.copySrcDirToDestDir( self.workdir, destdir )
    return True
