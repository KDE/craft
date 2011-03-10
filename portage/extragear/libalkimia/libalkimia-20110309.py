import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/office/alkimia/libalkimia'
        self.targets['4.3.0'] = 'libalkimia-4.3.0.tar.bz2'
        self.targetInstSrc['4.3.0'] = "libalkimia-4.3.0"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        #add the dependency when a proper package for libgmp will be available
        self.buildDependencies['win32libs-sources/mpir-src'] = 'default'
        self.shortDescription = "A library with common classes and functionality used by finance applications for the KDE SC."

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

    def fetch(self):
        if self.buildTarget == 'svnHEAD':
                CMakePackageBase.fetch(self)
        else:
                utils.wgetFile('"http://kde-apps.org/CONTENT/content-files/137323-libalkimia-4.3.0.tar.bz2"' , self.downloadDir() , "libalkimia-4.3.0.tar.bz2")
        return True

if __name__ == '__main__':
    Package().execute()
