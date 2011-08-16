from Package.BinaryPackageBase import *
import info
import shutil
import os
import utils


class subinfo(info.infoclass):
  def setTargets( self ):
    self.targets[ "gitHEAD" ]  =  "http://winkde.org/~pvonreth/downloads/ccache.tar.bz2"
    self.targetDigests['gitHEAD'] = '3533ff2854aa84b7d1c680747c1f01774cbe89e0'

    self.defaultTarget = "gitHEAD"


  def setDependencies( self ):
    self.hardDependencies['virtual/bin-base'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
