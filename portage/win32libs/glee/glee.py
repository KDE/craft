import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '5.4' ] = 'http://elf-stone.com/downloads/GLee/GLee5_4.zip'
        self.patchToApply[ '5.4' ] = ( "glee-src-5.4.diff", 1 )
        self.shortDescription = "GLee (GL Easy Extension library) is a free cross-platform extension loading library for OpenGL"
        self.defaultTarget = '5.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
