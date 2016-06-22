import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['7.0'] = "http://www.ijg.org/files/jpegsrc.v7.tar.gz"
        self.targetInstSrc['7.0'] = "jpeg-7"
        self.targets['8.0'] = "http://www.ijg.org/files/jpegsrc.v8.tar.gz"
        self.targets['8.0c'] = "http://www.ijg.org/files/jpegsrc.v8c.tar.gz"
        self.targets['9.0'] = "http://www.ijg.org/files/jpegsrc.v9.tar.gz"
        self.targets['9.0b'] = "http://www.ijg.org/files/jpegsrc.v9b.tar.gz"
        self.targetDigests['8.0c'] = 'f0a3b88ac4db19667798bee971537eeed552bce9'
        self.targetDigests['9.0b'] = (
        ['240fd398da741669bf3c90366f58452ea59041cacc741a489b99f2f6a0bad052'], EmergeHash.HashAlgorithm.SHA256)

        self.targetInstSrc['8.0'] = "jpeg-8"
        self.targetInstSrc['8.0c'] = "jpeg-8c"
        self.targetInstSrc['9.0'] = "jpeg-9"
        self.targetInstSrc['9.0b'] = "jpeg-9b"

        self.patchToApply['7.0'] = ( 'jpeg7.diff', 1 )
        self.patchToApply['8.0'] = ( 'jpeg8.diff', 1 )
        self.patchToApply['8.0c'] = ( 'jpeg8.diff', 1 )
        self.patchToApply['9.0'] = [( 'jpeg9.diff', 1 )]
        self.patchToApply['9.0b'] = [( 'jpeg-9b-20160618.diff', 1 )]

        self.shortDescription = 'A library for manipulating JPEG image format files'
        self.homepage = "http://www.ijg.org"

        self.defaultTarget = '9.0b'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

