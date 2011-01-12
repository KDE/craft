import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):   
        for ver in [ '9.0.2' ]:
            self.targets[ ver ] = 'http://btr0x2.rz.uni-bayreuth.de/packages/databases/PostgreSQL/source/v' + ver + '/postgresql-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'postgresql-' + ver
        self.shortDescription = "The Postgresql database server and libraries"
        self.defaultTarget = '9.0.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'

from Package.CMakePackageBase import *

class PackageMSVC( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        return True

    def compile( self ):       
        self.enterSourceDir()
        os.chdir( r"src\tools\msvc" )
        return self.system( "build.bat" )

    def install( self ):
        self.enterSourceDir()
        os.chdir( r"src\tools\msvc" )
        print self.imageDir()
        return self.system( "install.bat %s" % self.imageDir() )

from Package.AutoToolsPackageBase import *

class PackageMSys( AutoToolsPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__( self )
        self.shell = MSysShell()

#        self.buildInSource=True

      
if compiler.isMinGW():
    class Package( PackageMSys ):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package( PackageMSVC ):
        def __init__( self ):
            PackageMSVC.__init__( self )
            
if __name__ == '__main__':
    Package().execute()
