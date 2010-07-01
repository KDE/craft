import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepimlibs'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepimlibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepimlibs-4.0.' + ver
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
        self.hardDependencies['win32libs-sources/cyrus-sasl-src'] = 'default'
        self.hardDependencies['win32libs-sources/libical-src'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        self.hardDependencies['win32libs-bin/gpgme'] = 'default'

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
