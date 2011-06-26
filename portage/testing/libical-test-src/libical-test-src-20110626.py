import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'https://freeassociation.svn.sourceforge.net/svnroot/freeassociation/branches/windows-test/libical'
        self.defaultTarget = 'svnHEAD'
        self.shortDescription = "Testing package to test large windows changes and cmakeification"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DUSE_BUILTIN_TZDATA=true -DICAL_UNIX_NEWLINE=false "

if __name__ == '__main__':
    Package().execute()
