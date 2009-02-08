import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ( 0, 1, 2, 3, 4, 7 ):
            tgt = '0.8.%s' % i
            self.targets[ tgt ] = 'http://poppler.freedesktop.org/poppler-' + tgt + '.tar.gz'
            self.targetInstSrc[ tgt ] = 'poppler-' + tgt
        for i in ( '0.10.1', '0.10.2', '0.10.3' ):
          self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.gz' % i
          self.targetInstSrc[ i ] = 'poppler-%s' % i
        self.defaultTarget = "0.10.3"
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        if self.buildTarget == '0.8.0':
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
        self.doPackaging( "poppler", self.buildTarget, True )
        return True

if __name__ == '__main__':
    subclass().execute()
