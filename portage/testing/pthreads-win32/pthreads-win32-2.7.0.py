from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):     
        arch='32'
        if( os.getenv('EMERGE_ARCHITECTURE')=="x64"):
           arch='64'
        for version in ['2.7.0']:
            self.targets[ version ] = self.getPackageList("ftp.gnome.org/pub/gnome/binaries/win%s/dependencies"%arch,
                                                          ["pthreads-win32-2.7.0"".zip",
                                                          "pthreads-win32-dev-2.7.0"".zip"])
        self.targetDigests['2.7.0'] = ['92b3277254dd4bf604abf39299679bbed5c265ff',
                                       'e79812de0a3d13f4197cff72724097f709fe156f']
        self.defaultTarget = '2.7.0'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
    def __init__(self):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
    