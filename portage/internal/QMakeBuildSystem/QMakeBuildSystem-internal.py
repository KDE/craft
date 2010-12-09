import info
import os
import compiler

class subinfo(info.infoclass):
    def setDependencies( self ):
        utils.debug("emergebuildsystem:subinfo.setDependencies not implemented yet",1)
        # we need at least qmake 
        #self.dependencies['libs/qt'] = 'default'     
        if os.getenv( "EMERGE_MAKE_PROGRAM" ) != "":
            self.buildDependencies['dev-util/jom'] = 'default'

        if compiler.isMinGW():
            if compiler.isMinGW_W64():
                self.buildDependencies['dev-util/mingw-w64']    = 'default'
            elif compiler.isMinGW_ARM():
                self.buildDependencies['dev-util/cegcc-arm-wince'] = 'default'
            else:
                if compiler.isMinGW32():
                    self.buildDependencies['dev-util/mingw4']    = 'default'
                else:
                    self.buildDependencies['dev-util/mingw-w32']    = 'default'

from Package.InternalPackageBase import * 

class Package(InternalPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        InternalPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
