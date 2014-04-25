import info
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/cmake'] = 'default'
        self.buildDependencies['dev-util/jom'] = 'default'

        if compiler.isMinGW():
            if compiler.isMinGW_WXX():
                self.buildDependencies['dev-util/mingw-w64']    = 'default'

from Package.InternalPackageBase import *

class Package(InternalPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        InternalPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
