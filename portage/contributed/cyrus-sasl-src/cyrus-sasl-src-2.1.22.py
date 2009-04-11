import base
import utils
import os
import shutil
import info

# see http://wiki.mozilla.org/LDAP_C_SDK_SASL_Windows

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.1.22'] = 'ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-2.1.22.tar.gz'
        self.targetInstSrc['2.1.22'] = 'cyrus-sasl-2.1.22'
        self.patchToApply['2.1.22'] = ( 'cyrus-sasl-2.1.22.patch', 1 )
        self.defaultTarget = '2.1.22'

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
        return self.doPackaging( "cyrus-sasl", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
