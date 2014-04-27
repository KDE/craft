import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '3.08', '3.10', '3.14', '3.20', '3.31', '3.35' ]:
            self.targets[ ver ] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio' + ver.replace(".", "") + '0.tar.gz'
            self.targetInstSrc[ ver ] = "cfitsio"
        self.targetDigests['3.20'] = 'f200fe0acba210e88e230add6a4e68d80ad3d4f2'
        self.targetDigests['3.31'] = '35360dccc69dc5f12efb6fc9096ad951b59244d5'
        self.targetDigests['3.35'] = 'e928832708d6a5df21a1e17ae4a63036cab7c1b9'
        self.patchToApply['3.20'] = [("cfitsio-20101130.diff", 1)]
        self.patchToApply['3.31'] = [("cfitsio-20130124.diff", 1)]
        self.patchToApply['3.35'] = [("cfitsio-20130124.diff", 1)]

        self.shortDescription = "library for the FITS (Flexible Image Transport System) file format"
        self.defaultTarget = '3.35'

    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DENABLE_STATIC=ON"

if __name__ == '__main__':
    Package().execute()
