import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.8'] = """http://downloads.sourceforge.net/gnuwin32/gsl-1.8-bin.zip
                                 http://downloads.sourceforge.net/gnuwin32/gsl-1.8-lib.zip
                                 """
        self.targetDigests['1.8'] = ['91b42ab9fadc7da5eda18eb2b8f295cd89259df8',
                                     '20e597659098829eb6f46c9923c25bf2c7a47397']
        self.defaultTarget = '1.8'
            
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
