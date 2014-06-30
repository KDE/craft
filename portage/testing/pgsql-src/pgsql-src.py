import info
import compiler

class subinfo( info.infoclass ):
    def setTargets( self ):   
        for ver in [ '9.0.2' ]:
            self.targets[ ver ] = 'http://btr0x2.rz.uni-bayreuth.de/packages/databases/PostgreSQL/source/v' + ver + '/postgresql-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'postgresql-' + ver
            self.patchToApply[ ver ] = ('postgresql-' + ver + '-20110405.diff', '1')
        self.shortDescription = "The Postgresql database server and libraries"
        self.defaultTarget = '9.0.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

from Package.CMakePackageBase import *

class PackageMSVC( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

    def configure( self ):
        return True

    def make( self ):
        return True

    def compile( self ):
        self.enterSourceDir()
        os.chdir( r"src\tools\msvc" )
        
        # write the local config file which includes all the paths to the libraries
        f = open( "config.pl", "wb+" )
        f.write( """# configuration written by emerge\n"""
                 """use strict;\n"""
                 """use warnings;\n\n"""
                 """our $config;\n"""
                 """$config->{"openssl"}=\"""" + self.mergeDestinationDir().replace("\\", "\\\\") + """\";\n"""
#                 """$config->{"xml"}=\"""" + self.mergeDestinationDir().replace("\\", "\\\\") + """\";\n"""
#                 """$config->{"xslt"}=\"""" + self.mergeDestinationDir().replace("\\", "\\\\") + """\";\n"""
                 """$config->{"iconv"}=\"""" + self.mergeDestinationDir().replace("\\", "\\\\") + """\";\n"""
                 """$config->{"zlib"}=\"""" + self.mergeDestinationDir().replace("\\", "\\\\") + """\";\n"""
                 """\n1;\n""" )
        f.close()
        return self.system( "build.bat" )

    def install( self ):
        self.enterSourceDir()
        os.chdir( r"src\tools\msvc" )
        print(self.imageDir())
        return self.system( "install.bat %s" % self.imageDir() )

from Package.AutoToolsPackageBase import *

class PackageMSys( AutoToolsPackageBase ):
    def __init__( self ):
        AutoToolsPackageBase.__init__( self )

#        self.buildInSource=True

      
if compiler.isMinGW():
    class Package( PackageMSys ):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package( PackageMSVC ):
        def __init__( self ):
            PackageMSVC.__init__( self )
            
