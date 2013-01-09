import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://win-iconv.googlecode.com/svn/trunk'
        for ver in ['0.0.1', '0.0.2', '0.0.3', '0.0.4']:
            self.targets[ver] = 'http://win-iconv.googlecode.com/files/win-iconv-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'win-iconv-' + ver

        self.targetDigests['0.0.1'] = 'faf4f1f311f92f2a80afe275f43fabb047f23308'
        self.targetDigests['0.0.2'] = 'd61714a4708d76537600782eb72ccb3cbc89b4b5'
        self.targetDigests['0.0.3'] = '4af3a4b8632dfa35baca8a8ed57bb874f8ac4eb4'
        self.targetDigests['0.0.4'] = 'f9a5421f520a2fd37d6dbd1f7bf710ab67dec96b'
        self.patchToApply['0.0.2'] = ("win-iconv-0.0.2-20101217.diff", 1)
        self.shortDescription = "a character set conversion library binary compatible with GNU iconv"
        self.defaultTarget = '0.0.4'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        if emergePlatform.isCrossCompilingEnabled() and self.isTargetBuild():
            self.subinfo.options.configure.defines = "-DBUILD_STATIC=ON "

if __name__ == '__main__':
    Package().execute()
