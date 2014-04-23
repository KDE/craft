import os
import shutil

import utils
import info
import compiler


class subinfo( info.infoclass ):

    def setTargets( self ):
        # The deref version is a repackaged tarball of 1.0.0d
        # creation of this tarball was done on a secure machine
        # and the sources are exactly the same. Packaged
        # with GNU Tar options: tar --dereference -czf to avoid
        # problems with symlinks on windows
        
        # TODO: Patch this to use icl.exe when compiler.isIntel()
        # As this is pure C, there should be no problem with building it with cl.exe by now
        
        self.targets[ '1.0.0d' ] = ('https://downloads.sourceforge.net/project/kde-windows'
                                    '/openssl/1.0.0d/openssl-1.0.0d-orig-deref-src.tar.gz')
        self.targetInstSrc[ '1.0.0d' ] = 'openssl-1.0.0d'
        self.patchToApply['1.0.0d'] = ('openssl-1.0.0d.diff', 1)
        self.targetDigests['1.0.0d'] = '5c8472d09958c630eeb7548a1aeccb78fbd5cd10'

        for ver in [ '0.9.8k' , '0.9.8m' ,'1.0.0', '1.0.0a', '1.0.0b', '1.0.0c', '1.0.1c', '1.0.1e','1.0.1f','1.0.1g' ]:
            self.targets[ ver ] = 'http://www.openssl.org/source/openssl-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'openssl-' + ver
            if compiler.isMSVC() and ver not in [ '0.9.8k' , '0.9.8m' ,'1.0.0', '1.0.0a', '1.0.0b', '1.0.0c' ]:
              self.patchToApply[ ver ] = ('openssl-with-pdbs.diff', 1)
            self.targetDigestUrls[ ver ] = 'http://www.openssl.org/source/openssl-' + ver + '.tar.gz.sha1'
        self.targets[ '1.0.1-snapshot' ] = 'ftp://ftp.openssl.org/snapshot/openssl-1.0.1-stable-SNAP-20101028.tar.gz'
        self.shortDescription = "The OpenSSL runtime environment"

        self.defaultTarget = '1.0.1g'

        if compiler.isMinGW_W64():
            self.patchToApply[ '1.0.0' ] = ('openssl-1.0.0a-mingw64-asm.diff', 1)
            self.patchToApply[ '1.0.0a' ] = ('openssl-1.0.0a-mingw64-asm.diff', 1)
            self.patchToApply[ '1.0.0b' ] = ('openssl-1.0.0a-mingw64-asm.diff', 1)
            self.patchToApply[ '1.0.0c' ] = ('openssl-1.0.0a-mingw64-asm.diff', 1)
            self.patchToApply[ '1.0.0d' ] = ('openssl-1.0.0a-mingw64-asm.diff', 1)

    def setDependencies( self ):
            self.buildDependencies['virtual/base'] = 'default'
            self.buildDependencies['dev-util/perl'] = 'default'
            if compiler.isMinGW():
                self.buildDependencies['dev-util/msys'] = 'default'
                self.dependencies['win32libs/zlib'] = 'default'


from Package.CMakePackageBase import *

class PackageCMake(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.staticBuild = False

    def compile( self ):
        os.chdir( self.sourceDir() )
        cmd = ""
        if compiler.isX64():
            config = "VC-WIN64A"
        else:
            config = "VC-WIN32"

        if not self.system( "perl Configure %s" % config, "configure" ):
            return False

        if compiler.isX64():
            if not self.system( "ms\do_win64a.bat", "configure" ):
                return False
        else:
            if not self.system( "ms\do_ms.bat", "configure" ):
                return False


        if self.staticBuild:
            cmd = r"nmake -f ms\nt.mak"
        else:
            cmd = r"nmake -f ms\ntdll.mak"

        return self.system( cmd )

    def install( self ):
        src = self.sourceDir()
        dst = self.imageDir()

        if not os.path.isdir( dst ):
            os.mkdir( dst )
        if not os.path.isdir( os.path.join( dst, "bin" ) ):
            os.mkdir( os.path.join( dst, "bin" ) )
        if not os.path.isdir( os.path.join( dst, "lib" ) ):
            os.mkdir( os.path.join( dst, "lib" ) )
        if not os.path.isdir( os.path.join( dst, "include" ) ):
            os.mkdir( os.path.join( dst, "include" ) )

        if self.staticBuild:
            outdir = "out32"
        else:
            outdir = "out32dll"

        if not self.staticBuild:
            shutil.copy( os.path.join( src, outdir, "libeay32.dll" ) , os.path.join( dst, "bin" ) )
            shutil.copy( os.path.join( src, outdir, "ssleay32.dll" ) , os.path.join( dst, "bin" ) )
        shutil.copy( os.path.join( src, outdir, "libeay32.lib" ) , os.path.join( dst, "lib" ) )
        shutil.copy( os.path.join( src, outdir, "ssleay32.lib" ) , os.path.join( dst, "lib" ) )
        utils.copySrcDirToDestDir( os.path.join( src, "include" ) , os.path.join( dst, "include" ) )

        return True


from Package.AutoToolsPackageBase import *

class PackageMSys(AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.package.packageName = 'openssl'
        self.subinfo.options.package.packSources = False
        AutoToolsPackageBase.__init__(self)
        self.supportsCCACHE = False
        self.platform = ""

        self.buildInSource=True

        # target install needs perl with native path on configure time
        self.subinfo.options.configure.defines = " shared enable-md2 zlib-dynamic --with-zlib-lib=libzlib.dll.a --with-zlib-include=%s %s" % (
            self.shell.toNativePath(os.path.join( self.mergeDestinationDir() ,"include" )) ,compiler.getSimpleCompilerName() )
        if compiler.isMinGW32():
            self.subinfo.options.configure.defines += " -DOPENSSL_NO_CAPIENG"


    def install (self):
      self.enterSourceDir()
      self.shell.execute(self.sourceDir(), self.makeProgram, "INSTALLTOP=%s install_sw"  % (self.shell.toNativePath(self.imageDir())))
      self.shell.execute(os.path.join( self.imageDir() , "lib"), "chmod" ,"664 *")
      self.shell.execute(os.path.join( self.imageDir() , "lib" , "engines" ), "chmod" , "755 *")
      shutil.move( os.path.join( self.imageDir(),  "lib" , "libcrypto.dll.a" ) , os.path.join( self.imageDir() , "lib" , "libeay32.dll.a" ) )
      shutil.move( os.path.join( self.imageDir(), "lib" , "libssl.dll.a" ) , os.path.join( self.imageDir() , "lib" , "ssleay32.dll.a" ) )
      return True



if compiler.isMinGW():
    class Package(PackageMSys):
        def __init__( self ):
            PackageMSys.__init__( self )
else:
    class Package(PackageCMake):
        def __init__( self ):
            PackageCMake.__init__( self )

if __name__ == '__main__':
      Package().execute()

