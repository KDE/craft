import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://anongit.freedesktop.org/git/cairo'
        self.patchToApply['gitHEAD'] = [ ( "0001-add-cmake-support.patch", 1 ),
                                         ( "0002-win32-compile-fixes.patch", 1 ), 
                                         ( "0003-add-missing-file.patch", 1)
                                       ]

        self.shortDescription = "a 2D graphics library with support for multiple output devices"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/pixman'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
