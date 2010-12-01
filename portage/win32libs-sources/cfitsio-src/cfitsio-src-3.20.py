import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in [ '3.08', '3.10', '3.14', '3.20' ]:
            self.targets[ ver ] = 'ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio' + ver.replace(".", "") + '0.tar.gz'
            self.targetInstSrc[ ver ] = "cfitsio"
        self.targetDigests['3.20'] = 'f200fe0acba210e88e230add6a4e68d80ad3d4f2'
        self.patchToApply['3.20'] = ("cfitsio-20101130.diff", 1)
        self.shortDescription = "library for the FITS (Flexible Image Transport System) file format"
        self.shortDescription = "library for the FITS (Flexible Image Transport System) file format"
        self.defaultTarget = '3.20'

    def setDependencies( self ):
        self.buildDependencies['virtual/base']  = 'default'

from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DENABLE_STATIC=ON"
        
if __name__ == '__main__':
    Package().execute()
