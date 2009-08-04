import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.43'] = 'http://www.emmestech.com/software/pexports-0.43/pexports-0.43.zip'
        self.targetMergeSourcePath['0.43'] = 'pexports-0.43'
        self.defaultTarget = '0.43'
        self.options.merge.destinationPath = 'dev-utils'
        self.options.package.withCompiler = False

from Package.BinaryPackageBase import *        
        
class Package(BinaryPackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()



