import os
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/minsys'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

    def setTargets( self ):
        for ver in ['2.4.2']:
            self.targets[ver] = 'http://ftp.gnu.org/gnu/libtool/libtool-%s.tar.xz' % ver
            self.targetInstSrc[ver] = "libtool-%s" % ver
        self.targetDigests['2.4.2'] = '4671f3323f2fbc712a70afce57602ce906a82a15'

        self.defaultTarget = '2.4.2'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'msys'
        self.subinfo.options.configure.defines = "--enable-shared=no --enable-ltdl-install"
        self.subinfo.options.package.withCompiler = False

if __name__ == '__main__':
     Package().execute()
