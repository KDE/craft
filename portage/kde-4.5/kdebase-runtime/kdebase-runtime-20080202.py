import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdebase/runtime'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/runtime'
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'
        self.hardDependencies['win32libs-sources/libssh-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
