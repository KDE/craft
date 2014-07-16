import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '561' ] = 'http://www.cryptopp.com/cryptopp561.zip'
        self.patchToApply[ '561' ] = [('cmake.diff', 1),
                                      ('workaround_ice_31690.diff', 1),("cryptopp-5.6.1-gcc-4.7.0.patch",1)]
        self.targets[ '562' ] = 'http://www.cryptopp.com/cryptopp562.zip'
        self.patchToApply[ '562' ] = [('cmake.diff', 1)]
        self.targetDigests['561'] = '31dbb456c21f50865218c57b7eaf4c955a222ba1'
        self.targetDigests['562'] = 'ddc18ae41c2c940317cd6efe81871686846fa293'
        self.shortDescription = "Crypto++ Library is a free C++ class library of cryptographic schemes"
        self.homepage = "http://www.cryptopp.com/"
        self.defaultTarget = '562'


    def setDependencies( self ):
            self.buildDependencies['virtual/base'] = 'default'



from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DCRYPTOPP_BUILD_STATIC_LIBS=ON -DCRYPTOPP_BUILD_SHARED_LIBS=OFF -DCRYPTOPP_BUILD_TESTS=OFF"
         
        


