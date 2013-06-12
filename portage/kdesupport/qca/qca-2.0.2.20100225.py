
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/cyrus-sasl'] = 'default'

    def setTargets( self ):
        self.svnTargets['2.0.0-5'] = 'tags/qca/2.0.0'
        self.svnTargets['2.0.1-3'] = 'tags/qca/2.0.1'
        self.svnTargets['2.0.2-1'] = 'tags/qca/2.0.2'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/qca'
        self.targets['20130212'] = "http://downloads.sourceforge.net/kde-windows/qca-20130212.tar.xz"
        self.targetInstSrc['20130212'] = "qca-20130212"
        self.targetDigests['20130212'] = 'c87ef3cfe920fe331de156cf5dda297e835a1dfc'
        self.shortDescription = "Qt Cryptographic Architecture (QCA)"
        self.defaultTarget = '20130212'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()


