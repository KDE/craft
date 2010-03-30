import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/qjson/qjson.git'
        for ver in ['0.7.1']:
            self.targets[ ver ] = "http://downloads.sourceforge.net/qjson/qjson-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = "qjson"
        self.defaultTarget = '0.7.1'
        self.options.configure.defines = ""

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
