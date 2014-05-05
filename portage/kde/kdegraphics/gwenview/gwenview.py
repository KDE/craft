import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
            self.targetDigestUrls[ kd.kdeversion + ver  ] = 'http://download.kde.org/stable/' + kd.kdeversion + ver + '/src/' + self.package + '-' + kd.kdeversion + ver + '.tar.xz.sha1'
            self.patchToApply[kd.kdeversion + ver] = \
                [('0002-allow-compilation-with-jpeg9.patch', 1), # probably not to be upstreamed
                 ('0001-replace-usage-of-unportable-mkdtemp-with-KTempDir.patch', 1)] # https://git.reviewboard.kde.org/r/114181/

        self.patchToApply['gitHEAD'] = \
            [('0002-allow-compilation-with-jpeg9.patch', 1), # probably not to be upstreamed
             ('0001-replace-usage-of-unportable-mkdtemp-with-KTempDir.patch', 1)] # https://git.reviewboard.kde.org/r/114181/
        self.shortDescription = "Image viewer for KDE"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-baseapps'] = 'default'
        self.dependencies['kde/libkipi'] = 'default' 
        self.dependencies['win32libs/exiv2'] = 'default'
        self.dependencies['win32libs/jpeg'] = 'default'
   


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

