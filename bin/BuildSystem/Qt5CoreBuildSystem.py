#
# copyright (c) 2012 Patrick von Reth <vonreth@kde.org>
#
# definitions for the qt5 modules 

import os
import shutil

import utils
from BuildSystem.QMakeBuildSystem import *


class Qt5CoreBuildSystem( QMakeBuildSystem ):
    def __init__( self ):
        QMakeBuildSystem.__init__( self )
        utils.putenv( "QMAKESPEC", os.path.join( EmergeStandardDirs.emergeRoot( ), 'mkspecs', self.platform ) )


    def install( self, options = "" ):
        """implements the make step for Qt projects"""
        options += " INSTALL_ROOT=%s install" % self.imageDir( )[ 2: ]
        if not QMakeBuildSystem.install( self, options ):
            return False

        badPrefix = os.path.join( self.installDir( ), EmergeStandardDirs.emergeRoot( )[ 3: ] )
        if EmergeStandardDirs.emergeRoot( )[ 3: ] != "" and os.path.exists( badPrefix ):
            for subdir in os.listdir( badPrefix ):
                utils.moveFile( os.path.join( badPrefix, subdir ), self.installDir( ) )
            utils.rmtree( badPrefix )

        if os.path.exists( os.path.join( self.installDir( ), "bin", "mkspecs" ) ):
            utils.moveFile( os.path.join( self.installDir( ), "bin", "mkspecs" ),
                         os.path.join( self.installDir( ), "mkspecs" ) )

        #somehow qt stoped to install some achive files....
        if compiler.isMinGW( ):
            libdirSrc = os.path.join( self.buildDir( ), "lib" )
            libdirDest = os.path.join( self.imageDir( ), "lib" )
            for archive in os.listdir( libdirSrc ):
                if archive.endswith( ".a" ) and not os.path.exists( os.path.join( libdirDest, archive ) ):
                    utils.copyFile( os.path.join( libdirSrc, archive ), os.path.join( libdirDest, archive ), False )
        return True



          

