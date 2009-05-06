import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '0.2.0', '0.2.1' ]:
          self.targets[v] = 'http://poppler.freedesktop.org/poppler-data-' + v + '.tar.gz'
          self.targetInstSrc[v] = 'poppler-data-' + v
          self.patchToApply[v] = ( 'poppler-data-cmake.patch', 0 )
        self.defaultTarget = '0.2.1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def compile( self ):
        self.kdeCompile()
        return True
        
    def install( self ):
        self.kdeInstall()
        return True
        
    def make_package( self ):
        # now do packaging with kdewin-packager
        self.doPackaging( "poppler-data", self.buildTarget, True )

        return True

if __name__ == '__main__':
    subclass().execute()
