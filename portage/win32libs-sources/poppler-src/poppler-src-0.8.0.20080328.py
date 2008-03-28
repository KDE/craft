import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.6.4'] = 'http://poppler.freedesktop.org/poppler-0.6.4.tar.gz'
        self.targetInstSrc['0.6.4'] = 'poppler-0.6.4'
        self.targets['0.7.1'] = 'http://poppler.freedesktop.org/poppler-0.7.1.tar.gz'
        self.targetInstSrc['0.7.1'] = 'poppler-0.7.1'
        self.targets['0.7.2'] = 'http://poppler.freedesktop.org/poppler-0.7.2.tar.gz'
        self.targetInstSrc['0.7.2'] = 'poppler-0.7.2'
        self.targets['0.8.0'] = 'http://poppler.freedesktop.org/poppler-0.8.0.tar.gz'
        self.targetInstSrc['0.8.0'] = 'poppler-0.8.0'
        self.defaultTarget = '0.8.0'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-sources/fontconfig-src'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        if self.buildTarget == '0.6.4':
            src = os.path.join( self.workdir, self.instsrcdir )

            cmd = "cd %s && patch -p0 < %s" % \
                  ( self.workdir, os.path.join( self.packagedir , "poppler-cmake.patch" ) )
            if utils.verbose() >= 1:
                print cmd
            self.system( cmd ) or die( "patch" )
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir , "poppler-pagetransition.diff" ) )
        if utils.verbose() >= 1:
            print cmd
        self.system( cmd ) or die( "patch" )
            
        return True
        
        
    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_QT4_TESTS=ON"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def kdeSvnPath( self ):
        return False
        
    def make_package( self ):
        # now do packaging with kdewin-packager
        self.doPackaging( "poppler", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
