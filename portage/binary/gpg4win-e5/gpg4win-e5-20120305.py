# GnuPG - Windows development package
#
# This Package contains the headers and libraries for the gnupg software:
#
# libgpg-error
# libgcrypt
# libassuan
# libksba
# gpgme
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
        version="201507081029"
        self.targets[version] = \
                "http://files.kolab.org/local/gpg4win/gpg4win-dev-"+version+".tar.bz2"
        self.defaultTarget = version
        self.targetDigests[version] = 'e67e160af3d3f1373b6a9e5eb27582ef1123d2a0'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
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
