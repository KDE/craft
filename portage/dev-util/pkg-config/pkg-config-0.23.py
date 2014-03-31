from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        #from http://kemovitra.blogspot.com/2009/07/mingw-building-static-pkg-config.html
        self.targets[ '0.23' ]          = 'http://downloads.sourceforge.net/kde-windows/pkg-config.exe'
        self.targetDigests['0.23'] = '4a00011073670fc68817d730db0f2187f6343d8c'
        self.defaultTarget = '0.23'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )
    self.subinfo.options.merge.destinationPath = 'dev-utils/bin'

if __name__ == '__main__':
    Package().execute()