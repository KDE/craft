# -*- coding: utf-8 -*-
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):        
        self.shortDescription = "The Qwt library contains GUI Components and utility classes which are primarily useful for programs with a technical background"
        for ver in ["6.0.1"]:
            self.targets[ver] = "http://downloads.sourceforge.net/sourceforge/qwt/qwt-%s.tar.bz2" % ver
            self.targetInstSrc[ver] = "qwt-%s" % ver
        self.targetDigests['6.0.1'] = '301cca0c49c7efc14363b42e082b09056178973e'
        self.defaultTarget = "6.0.1"

    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'


from Package.QMakePackageBase import *

class Package( QMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        QMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ' "QWT_INSTALL_PREFIX = %s" ' % self.imageDir().replace("\\","/")
        
    def install( self ):
        if not QMakePackageBase.install( self ):
            return False
        #sic.: the .lib file is placed under bin dir in hupnp)
        os.mkdir( os.path.join( self.installDir(), "bin" ) )
        # copy over dlls as required by KDE convention
        for file in os.listdir( os.path.join( self.installDir(), "lib" ) ):
            if file.endswith( ".dll" ):
                utils.copyFile( os.path.join( self.installDir(), "lib" , file ), os.path.join( self.installDir(), "bin" , file ) )
        return True
        

        
if __name__ == '__main__':
    Package().execute()
