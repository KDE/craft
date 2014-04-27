# -*- coding: utf-8 -*-
import info

from Package.QMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.defaultTarget = '0.97'
        self.shortDescription = "kQOAuth is a library written in C++ for Qt that implements the OAuth 1.0 authentication specification RFC 5849"

        self.svnTargets['gitHEAD'] = 'https://github.com/kypeli/kQOAuth.git'
        
        for ver in ['0.97']:
            self.targets[ver] ='https://github.com/kypeli/kQOAuth/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'kQOAuth-' + ver
        
        self.targetDigests['0.97'] = '76a4556c49b07a101927ef50e1eaa994cabd3bf7'
        
        self.patchToApply['0.97'] = ('kqoauth-no-examples-or-tests.diff', 1)
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        QMakePackageBase.__init__( self )
        
    def install( self ):
        #This doesn't work properly...
        # if not QMakePackageBase.install( self ):
            # return False
        #...so manually install to image directory which is then copied into kderoot
        os.makedirs( os.path.join( self.installDir(), "bin" ) )
        os.makedirs( os.path.join( self.installDir(), "lib" ) )
        os.makedirs( os.path.join( self.installDir(), "include", "QtKOAuth" ) )
        os.makedirs( os.path.join( self.installDir(), "mkspecs", "features" ) )
        # copy over dlls, libs, and includes as required by KDE convention
        for file in os.listdir( os.path.join( self.buildDir(), "lib" ) ):
            if file.endswith( ".dll" ):
                utils.copyFile( os.path.join( self.buildDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
            elif file.endswith( ".lib" ) or file.endswith( ".prl" ) or file.endswith( ".pdb" ):
                utils.copyFile( os.path.join( self.buildDir(), "lib" , file ), os.path.join( self.installDir(), "lib" , file ) )
        for file in os.listdir( os.path.join( self.sourceDir(), "src" ) ):
            if file.endswith( ("kqoauthrequest.h", "kqoauthrequest_1.h", "kqoauthrequest_xauth.h", "kqoauthmanager.h", "kqoauthglobals.h") ):
                utils.copyFile( os.path.join( self.sourceDir(), "src" , file ), os.path.join( self.installDir(), "include" , "QtKOAuth", file ) )
        utils.copyFile( os.path.join( self.sourceDir(), "include" , "QtKOAuth" ), os.path.join( self.installDir(), "include" , "QtKOAuth", "QtKOAuth" ) )
        utils.copyFile( os.path.join( self.sourceDir(), "kqoauth.prf" ), os.path.join( self.installDir(), "mkspecs" , "features", "kqoauth.prf" ) )
        return True
        

if __name__ == '__main__':
    Package().execute()
