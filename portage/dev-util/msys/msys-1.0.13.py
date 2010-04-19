import info


class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/sourceforge/mingw"""
        msysFiles=""
        for file in ['msysCORE-1.0.13-2-msys-1.0.13-bin.tar.lzma',
                     'bash-3.1.17-2-msys-1.0.11-bin.tar.lzma',
                     'sed-4.2.1-1-msys-1.0.11-bin.tar.lzma',
                     'coreutils-5.97-2-msys-1.0.11-bin.tar.lzma',
                     'gawk-3.1.7-1-msys-1.0.11-bin.tar.lzma',
                     'make-3.81-2-msys-1.0.11-bin.tar.lzma',
                     'grep-2.5.4-1-msys-1.0.11-bin.tar.lzma']:
            msysFiles = """%s
                        %s/%s""" % ( msysFiles , repoUrl , file )
        self.targets['1.0.13'] = msysFiles
        self.targetDigests['1.0.13'] = ['fff020614bd796697739887c636f15a42b4b14aa',
                                        'd068b4a415c46801b7fa1c50c2e9e07bb0c09d1d',
                                        '9b92104c8182b4ef5f155aa887f606adeae11d08',
                                        '01007bff4cf8a21740bb9e5bb9bf8745f83a81b1',
                                        '521f076f6db7c8415698b4999baca99ab8754de1',
                                        '0752b40a23f312523239b629af62be0a7ffee746',
                                        '1bde43d6f06173ffb8c0764f13f2345667c99ad0']
        self.defaultTarget = '1.0.13'
        # This attribute is in prelimary state
        ## \todo move to dev-utils/msys
        self.targetMergePath['1.0.13'] = "msys";
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
