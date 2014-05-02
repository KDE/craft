import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
            self.targetDigestUrls[ kd.kdeversion + ver  ] = 'http://download.kde.org/stable/' + kd.kdeversion + ver + '/src/' + self.package + '-' + kd.kdeversion + ver + '.tar.xz.sha1'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        # these dependencies are optional
        #self.dependencies['kdesupport/poppler'] = 'default'
        #self.dependencies['win32libs/taglib'] = 'default'
        #self.dependencies['win32libs/exiv2'] = 'default'
        ##self.dependencies['win32libs/ffmpeg'] = 'default'

        # this is required
        self.dependencies['kde/kdelibs'] = 'default'
        self.shortDescription = "baloo support library"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

