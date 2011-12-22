import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        # not used  yet only for reference
        self.targets[ '0.0.2' ] = "http://download.microsoft.com/download/1/1/1/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe"
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
            if compiler.isMinGW32():
                srcdir = os.path.join( self.rootdir, "mingw", "bin" )
                files = [ 'mingwm10.dll', 'libgcc_s_dw2-1.dll' ]
            elif compiler.isMinGW_W32():
                srcdir = os.path.join( self.rootdir, "mingw", "bin" )
                files = [ 'libgcc_s_sjlj-1.dll', 'libgomp-1.dll' ]
            elif compiler.isMinGW_W64():
                srcdir = os.path.join( self.rootdir, "mingw64", "bin" )
                files = [ 'libgcc_s_sjlj-1.dll', 'libgomp-1.dll' ]
#        elif compiler.isMSVC2008():
#            if self.buildType() == "Debug":
#                srcdir = os.path.join( self.packageDir(), "redist", "Debug_NonRedist", "x86", "Microsoft.VC90.DebugCRT" )
#                files = [ "Microsoft.VC90.DebugCRT.manifest", "msvcr90d.dll", "msvcp90d.dll", "msvcm90d.dll"]
#            else:
#                srcdir = os.path.join( self.packageDir(), "redist", "x86", "Microsoft.VC90.CRT" )
#                files = [ "Microsoft.VC90.CRT.manifest", "msvcr90.dll", "msvcp90.dll", "msvcm90.dll" ]
        elif compiler.isMSVC2010():
            if self.buildType() == "Debug":
                srcdir = os.path.join( os.environ["VCINSTALLDIR"], "redist", "Debug_NonRedist" , os.environ["EMERGE_ARCHITECTURE"] , "Microsoft.VC100.DebugCRT"  ) 
            else:
                srcdir = os.path.join( os.environ["VCINSTALLDIR"], "redist", os.environ["EMERGE_ARCHITECTURE"] , "Microsoft.VC100.CRT" ) 
            files = [ "msvcr100%s.dll" % postfix, "msvcp100%s.dll" % postfix ]

        for file in files:
            utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )

        # extract pthread package.
        if compiler.isMinGW_WXX():
            tmpdir = os.getenv( "TEMP" )

            if compiler.isMinGW_W32(): _ext = ("mingw", 32)
            elif compiler.isMinGW_W64(): _ext = ("mingw64", 64)
            else: utils.die( "unknown flavor of mingw-wXX" )

            pthreadPackageName = os.path.join( self.rootdir, "%s", "pthreads-w%s.zip" ) % _ext
            pthreadDll = "pthreadGC2-w%s.dll" % _ext[1]

            utils.unZip( pthreadPackageName, tmpdir )

            srcdir = os.path.join( tmpdir, "bin" )
            files = [ pthreadDll ]
            for file in files:
                utils.copyFile( os.path.join( srcdir, file ), os.path.join( destdir, file ) )
        return True

if __name__ == '__main__':
    Package().execute()
