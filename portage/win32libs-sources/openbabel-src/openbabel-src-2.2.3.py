import base
import os
import utils
import info

#
# this library is used by kdeedu/kalzium
#

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.2.0'] = 'http://downloads.sourceforge.net/sourceforge/openbabel/openbabel-2.2.0.tar.gz'
        self.targets['2.2.3'] = 'http://downloads.sourceforge.net/sourceforge/openbabel/openbabel-2.2.3.tar.gz'
        self.patchToApply['2.2.0'] = ('openbabel-2.2.0-cmake.diff', 0)
        self.targetInstSrc['2.2.0'] = 'openbabel-2.2.0'
        self.targetInstSrc['2.2.3'] = 'openbabel-2.2.3'
        self.defaultTarget = '2.2.3'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "openbabel", self.buildTarget )

if __name__ == '__main__':
    subclass().execute()
