# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs/libvorbis'] = 'default'
        self.hardDependencies['win32libs/openal-soft'] = 'default'
        self.hardDependencies['win32libs/sqlite'] = 'default'
        self.hardDependencies['win32libs/freetype'] = 'default'
        self.hardDependencies['win32libs/irrlicht'] = 'default'
        self.shortDescription = 'A very fun Free Software minecraft clone'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/minetest/minetest.git'
        self.patchToApply['gitHEAD'] = ('minetest-20130413.patch', 1)
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DENABLE_FREETYPE=TRUE -D"

if __name__ == '__main__':
    Package().execute()
