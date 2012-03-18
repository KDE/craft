import info

class subinfo( info.infoclass ):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.targets['0.1.0'] = 'http://qtscriptgenerator.googlecode.com/files/qtscriptgenerator-src-0.1.0.tar.gz'
        self.targetInstSrc['0.1.0'] = 'qtscriptgenerator-src-0.1.0'
        self.targetDigests['0.1.0'] = 'eeae733106369e289f257b754822bc372fd6ba75'
        self.patchToApply['0.1.0'] = [("qtscriptgenerator-cmake.diff", 1),
                                      ("qtscriptgenerator.diff", 1),
                                      ("qtscriptgenerator.gcc-4.4.diff", 1),
                                      ("qtscriptgenerator-0.1.0-qt48.diff",1)]
        self.shortDescription = "a tool that generates Qt bindings for Qt Script"
        self.defaultTarget = '0.1.0'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
