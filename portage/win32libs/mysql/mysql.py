import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/perl'] = 'default'
        self.buildDependencies['gnuwin32/bison'] = 'default'

    def setTargets( self ):
        for ver in ['5.6.26']:
            self.targets[ ver ] = 'http://cdn.mysql.com/Downloads/MySQL-5.6/mysql-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'mysql-' + ver
        self.patchToApply['5.6.26'] = [("mysql-5.6.26-20150923.diff", 1)]
        self.targetDigests['5.6.26'] = '1f266a2782e13d4f5a2614d91ed5861e524c9467'
        self.shortDescription = "mysql"
        self.defaultTarget = '5.6.26'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        # both examples and tests can be run here
        self.subinfo.options.configure.defines = "-DWITH_UNIT_TESTS=OFF"
        #self.subinfo.options.configure.testDefine = "-DBUILD_tests=ON  -DBUILD_examples=ON"
        #self.subinfo.options.configure.toolsDefine = "-DBUILD_tools=ON" # available only from 2.1.0-beta3
        #self.subinfo.options.configure.staticDefine = "-DBUILD_shared=OFF" # available only from 2.1.0-beta3

