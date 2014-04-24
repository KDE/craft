import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        # not used  yet only for reference
        self.targets['0.0.2'] = "http://download.microsoft.com/download/5/B/C/5BC5DBB3-652D-4DCE-B14A-475AB85EEF6E/vcredist_x86.exe"
        self.shortDescription = "the compiler runtime package"
        self.defaultTarget = '0.0.2'

    def setDependencies( self ):
        self.buildDependencies[ 'virtual/base' ] = 'default'

from Package.BinaryPackageBase import *
import compiler


class Package( BinaryPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        if compiler.isMinGW():
            self.subinfo.options.package.version = compiler.getMinGWVersion()
#        elif compiler.isMSVC2008():
#            self.subinfo.options.package.version = '9.0.30729.1'

    def fetch( self ):
        return True

    def unpack( self ):
        destdir = os.path.join( self.installDir(), "bin" )
        utils.createDir( self.workDir() )
        utils.createDir( destdir )

        postfix = ""
        if self.buildType() == "Debug":
            postfix = "d"

        files = []
        if compiler.isMinGW():
            if self.subinfo.options.features.legacyGCC:
                if compiler.isMinGW_W32():
                    srcdir = os.path.join( self.rootdir, "mingw", "bin" )
                elif compiler.isMinGW_W64():
                    srcdir = os.path.join( self.rootdir, "mingw64", "bin" )
                files = [ 'libgcc_s_sjlj-1.dll', 'libgomp-1.dll' ]
            else:                
                files = [ 'libgomp-1.dll', 'libstdc++-6.dll', 'libwinpthread-1.dll' ]
                if compiler.isMinGW_W32():
                    files.append('libgcc_s_sjlj-1.dll')
                    srcdir = os.path.join( self.rootdir, "mingw", "bin" )                    
                elif compiler.isMinGW_W64():
                    files.append('libgcc_s_seh-1.dll')
                    srcdir = os.path.join( self.rootdir, "mingw64", "bin" )
                
        elif compiler.isMSVC2010():
            if compiler.isX86() and os.environ["PROCESSOR_ARCHITECTURE"] == "AMD64":
                srcdir = os.path.join( os.environ["SystemRoot"], "SysWOW64") 
            else:
                srcdir = os.path.join( os.environ["SystemRoot"], "System32") 
            files = [ "msvcr100%s.dll" % postfix, "msvcp100%s.dll" % postfix ]

        for file in files:
            utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) ,False)       

        return True

if __name__ == '__main__':
    Package().execute()
