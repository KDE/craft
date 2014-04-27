# This package is in testing for a good reason it installs
# several things into your emerge root directory which will
# include openssl for example and can break your builds!

from Package.CMakePackageBase import *
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        versions = ["9.0.4-1"]

        for version in versions:
            self.targets[version] = (
                    "http://get.enterprisedb.com/postgresql/postgresql-"
                    "%s-windows-binaries.zip" % version)
            self.targetInstSrc[version] = "pgsql"

        self.targetDigests['9.0.4-1'] = '80edae9c8c03ea05f1775c8de7fe70391f624ee7'
        self.shortDescription = "Postgresql database and libraries"
        self.options.package.withCompiler = False
        self.defaultTarget = '9.0.4-1'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__( self )

    def compile( self ):
        return True

    def install( self ):
        if( not self.cleanImage()):
            return False

        shutil.copytree(self.sourceDir() , self.installDir())

        return True
