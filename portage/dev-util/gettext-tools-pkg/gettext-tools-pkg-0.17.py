from Package.BinaryPackageBase import *
import os
import info
import platform

class subinfo(info.infoclass):
    def setTargets( self ):
        if(platform.buildArchitecture() == 'x64' ):
          self.targets['0.17'] ='http://ftp.acc.umu.se/pub/gnome/binaries/win64/dependencies/gettext-tools-dev_0.17-3_win64.zip'
          self.targetDigests['0.17'] = 'f970e1b6b3810fb5aca3279c6c2634e75f29342f'
        else:
          self.targets['0.17'] = 'http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/gettext-tools-0.17.zip'

        self.defaultTarget = '0.17'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )
    self.subinfo.options.merge.destinationPath = 'dev-utils'
    self.subinfo.options.merge.ignoreBuildType = True
    self.subinfo.options.package.packSources = False
    self.subinfo.options.package.withCompiler = None

if __name__ == '__main__':
    Package().execute()
