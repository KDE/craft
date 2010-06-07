import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.14-1'] = self.getPackageList('http://downloads.sourceforge.net/sourceforge/mingw',
                                                 ['msysCORE-1.0.14-1-msys-1.0.14-bin.tar.lzma',
                                                 'bash-3.1.17-3-msys-1.0.13-bin.tar.lzma',
                                                 'libregex-1.20090805-2-msys-1.0.13-dll-1.tar.lzma',
                                                 'libtermcap-0.20050421_1-2-msys-1.0.13-dll-0.tar.lzma',
                                                 'termcap-0.20050421_1-2-msys-1.0.13-bin.tar.lzma',
                                                 'sed-4.2.1-2-msys-1.0.13-bin.tar.lzma',
                                                 'coreutils-5.97-3-msys-1.0.13-bin.tar.lzma',
                                                 'gawk-3.1.7-2-msys-1.0.13-bin.tar.lzma',
                                                 'make-3.81-3-msys-1.0.13-bin.tar.lzma',
                                                 'grep-2.5.4-2-msys-1.0.13-bin.tar.lzma',
                                                 'libintl-0.17-2-msys-dll-8.tar.lzma',
                                                 'libiconv-1.13.1-2-msys-1.0.13-dll-2.tar.lzma'])
                                                 
        self.targetDigests['1.0.14-1'] = ['13d7ee49f1f0b94884f52f877edb04f7af85522b',
                                         'c2d029aedc7dda6e7da3aa83621293b66a498a73',
                                         'd95faa144cf06625b3932a8e84ed1a6ab6bbe644',
                                         'e4273ccfde8ecf3a7631446fb2b01971a24ff9f7',
                                         'c8e450e6dd6109bbcee53cfe5379c49a7daf110a',
                                         'ced60ab96ab3f713da0d0a570232f2a5f0ec5270',
                                         '54ac256a8f0c6a89f1b3c7758f3703b4e56382be',
                                         '421ecc23e764ed87291796501189cc92fa905c0d',
                                         'c7264eb13b05cf2e1a982a3c2619837b96203a27',
                                         '69d03c4415c55b9617850a4991d0708fbe3788f6',
                                         'f4fd249ff5810b01fedc4a1dbdbe1b7d1e4cc619',
                                         '2b64c42ac61c7ebd710333a6db2f35b21e4fccaf']


   
        self.defaultTarget = '1.0.14-1'
        # This attribute is in prelimary state
        ## \todo move to dev-utils/msys
        self.targetMergePath['1.0.14-1'] = "msys";
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
