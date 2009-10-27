import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svn'] = 'branches/work/akonadi-ports/kdepimlibs/'
        self.defaultTarget = 'svn'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/libical'] = 'default'
        self.hardDependencies['win32libs-bin/gpgme'] = 'default'
        self.hardDependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

if __name__ == '__main__':
    Package().execute()
