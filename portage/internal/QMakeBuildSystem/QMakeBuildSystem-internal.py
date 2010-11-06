import info
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        utils.debug("emergebuildsystem:subinfo.setDependencies not implemented yet",1)
        # we need at least qmake 
        #self.hardDependencies['libs/qt'] = 'default'     
        if (os.getenv( "KDECOMPILER" ) == "msvc2008" or os.getenv( "KDECOMPILER" ) == "msvc2005" or os.getenv( "KDECOMPILER" ) == "msvc2010") and os.getenv( "EMERGE_MAKE_PROGRAM" ) != "":
            self.hardDependencies['dev-util/jom'] = 'default'

        # find a way to share this with other build systems
        if os.getenv( "KDECOMPILER" ) == "mingw4":
            if emergePlatform.buildArchitecture() == 'x64':
                self.hardDependencies['dev-util/mingw-w64']    = 'default'
            elif emergePlatform.buildArchitecture() == 'arm-wince':
                self.hardDependencies['dev-util/cegcc-arm-wince'] = 'default'
            else:
                self.hardDependencies['dev-util/mingw4']    = 'default'

from Package.InternalPackageBase import * 

class Package(InternalPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        InternalPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
