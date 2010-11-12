import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/msys'] = 'default'     
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['dev-util/autotools'] = 'default'        

from Package.InternalPackageBase import * 

class Package(InternalPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        InternalPackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()
