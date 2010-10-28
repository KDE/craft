import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        utils.debug("emergebuildsystem:subinfo.setDependencies not implemented yet",1)
        #    #self.hardDependencies['libs/qt'] = 'default'     

from Package.InternalPackageBase import * 

class Package(InternalPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        InternalPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
