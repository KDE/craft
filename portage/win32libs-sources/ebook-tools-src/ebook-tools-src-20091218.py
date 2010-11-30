# -*- coding: utf-8 -*-
import info
import compiler

# attention: if you want to build ebook-tools with msvc, please apply the msvc-toC89.diff patch first
# currently msvc gets problems when compiling it

class subinfo(info.infoclass):
    def setTargets( self ):
        svnurl = "https://ebook-tools.svn.sourceforge.net/svnroot/ebook-tools/"
        self.svnTargets['svnHEAD'] = svnurl + 'trunk/ebook-tools'
        for ver in ['0.1.1', '0.2.1']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/ebook-tools/ebook-tools-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'ebook-tools-' + ver
            self.patchToApply[ ver ] = [('ebook-tools-' + ver + '.diff', 1)]
        if compiler.isMSVC():
            self.patchToApply['0.1.1'].append(('msvc-toC89.diff', 1))
        self.targetDigests['0.2.1'] = '1340eb7141b453088d39e62bba771413053a6d18'
        self.shortDescription = "Tools for accessing and converting various ebook file formats"
        self.defaultTarget = '0.2.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libzip'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()