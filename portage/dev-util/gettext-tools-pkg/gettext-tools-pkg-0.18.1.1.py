import info
from shells import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.18.1.1'] = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.18.1.1.tar.gz'
        self.targetDigests['0.18.1.1'] = '5009deb02f67fc3c59c8ce6b82408d1d35d4e38f'
        self.targetInstSrc['0.18.1.1'] = 'gettext-0.18.1.1'
        self.defaultTarget = '0.18.1.1'
        
    def setDependencies( self ):
        self.dependencies['dev-util/perl'] = 'default' # buildtime dependency
        self.dependencies['dev-util/msys'] = 'default' # buildtime dependency
        self.dependencies['win32libs-bin/win_iconv'] = 'default'


from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.defines = "--disable-java --disable-csharp --disable-shared --enable-static --with-gettext-tools "


if __name__ == '__main__':
     Package().execute()
