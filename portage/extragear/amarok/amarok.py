# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '2.3.1', '2.3.2', '2.4.3', '2.5.0', '2.6.0', '2.7.0', '2.8.0' ]:
            self.targets[ver] = 'http://download.kde.org/download.php?url=stable/amarok/' + ver + '/src/amarok-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'amarok-' + ver
        self.patchToApply[ '2.3.2' ] = [ ( 'amarok-2.3.2-20110110.diff', 1 ) ]
        self.patchToApply[ '2.4.3' ] = [ ( 'amarok-2.4.3-20110818.diff', 1 ), ( 'amarok-2.4.3-x64.diff', 1 ) ]
        self.targetDigests['2.4.3'] = '8a46fca6a550a4ca403a9be7f595728c819641c4'
        self.patchToApply[ '2.5.0' ] = [ ( 'amarok-2.4.90-20111208.diff', 1 )]
        self.targetDigests['2.5.0'] = '9849900d20225e703c43d242650a8fa211cf15f2'
        self.patchToApply[ '2.7.0' ] = [( 'no_cd_collection.patch', 1),
                                        ( 'amarok-2.7.0-fix-compilation-with-MSCV-2010.patch', 1 ),
                                        ( 'mysqle-location-fix.diff', 1)]
                                        
                                        
        self.targetDigests['2.7.0'] = 'd0ae4a2cb81a54ae94ca24fdb3aed88d7f3a921e'
        self.patchToApply[ '2.8.0' ] = [( '0001-Don-t-communicate-with-mysql-by-env-vars-and-autogen.patch', 1),
                                        ( '0001-Don-t-add-the-analyzer-applet-when-Phonon-doesn-t-su.patch', 1)]

        self.svnTargets['gitHEAD'] = '[git]kde:amarok.git'
        self.defaultTarget = '2.8.0'

    def setDependencies( self ):
        self.dependencies['win32libs/taglib'] = 'default'
        self.dependencies['win32libs/taglib-extras'] = 'default'
        self.dependencies['qt-libs/phonon'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['qt-libs/liblastfm'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.runtimeDependencies['kdesupport/qtscriptgenerator'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.shortDescription = "a powerful music player"

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)


