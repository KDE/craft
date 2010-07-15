# GnuPG - Windows development package
#
# This Package contains the headers and libraries for the gnupg software:
# 
# libgpg-error-1.8
# libgcrypt-1.4.5
# libassuan-2.0.0
# libksba-1.0.7
# gpgme-1.3.0
#
# The intention is that they should keep up with the recent versions of gpg4win
# (www.gpg4win.de) which packages gnupg seperatly so KDE software can interact
# with gpg4win.

from Package.CMakePackageBase import *
import info
import glob
import compiler

class subinfo(info.infoclass):

    def setTargets( self ):
        version="20100611"
        self.targets[version] = \
            "ftp://ftp.gnupg.org/gcrypt/binary/gpg-w32-dev-"+version+".zip"
        self.defaultTarget = version
        self.targetDigests[version] = 'dd0fe2b83d102d906563e47e488014b20c85462f'
        self.targetInstSrc[version] = "gpg-w32-dev-"+version

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['contributed/gpg-wce-dev'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(CMakePackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.package.packSources = False
        self.subinfo.options.package.withCompiler = None
        CMakePackageBase.__init__( self )

    def compile( self ):
        return True

    def install( self ):
        if( not self.cleanImage()):
            return False
    # This package is built with MinGW gcc, since the msvc expects a different
    # Name it shall get it.
        if compiler.isMSVC():
            gcc_names = glob.glob( self.sourceDir() + '/lib/*.dll.a' )
            for gcc_name in gcc_names:
                msvc_name = gcc_name.replace( ".dll.a", ".lib" )
                shutil.move(gcc_name, msvc_name)
        shutil.copytree( self.sourceDir() , self.installDir() )
        return True

if __name__ == '__main__':
    Package().execute()
