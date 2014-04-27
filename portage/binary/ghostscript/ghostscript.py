from Package.BinaryPackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['8.64', '9.00']:
            self.targets[ version ] = self.getUnifiedPackage( repoUrl, "ghostscript", version )


        self.defaultTarget = '9.00'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(BinaryPackageBase):
  def __init__(self):
    BinaryPackageBase.__init__( self )
    self.subinfo.options.package.withCompiler = False
    self.subinfo.options.package.withSources = False

if __name__ == '__main__':
    Package().execute()
