# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        svnurl = "https://ebook-tools.svn.sourceforge.net/svnroot/ebook-tools/"
        self.svnTargets['svnHEAD'] = svnurl + 'trunk/ebook-tools'
        self.targets['0.1.1'] = 'http://downloads.sourceforge.net/ebook-tools/ebook-tools-0.1.1.tar.gz'
        self.targetInstSrc['0.1.1'] = 'ebook-tools-0.1.1'
        self.patchToApply['0.1.1'] = ('ebook-tools-0.1.1.diff', 1)
        self.defaultTarget = '0.1.1'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-sources/libzip-src'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()