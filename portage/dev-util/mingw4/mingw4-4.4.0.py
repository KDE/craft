import base
import utils
import shutil
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.3.0'] =  self.getPackageList('http://downloads.sourceforge.net/sourceforge/mingw',
                                                   ['binutils-2.18.50-20080109-2.tar.gz',
                                                   'gcc-4.3.0-20080502-mingw32-alpha-bin.tar.gz,'
                                                   'mingw32-make-3.81-20080326.tar.gz',
                                                   'mingw-runtime-3.14.tar.gz',
                                                   'w32api-3.11.tar.gz',
                                                   'gdb-6.8-mingw-3.tar.bz2',
                                                   'mingw-utils-0.3.tar.gz'])
        self.targetMergePath['4.3.0'] = "mingw";
		  
        self.targets['4.4.0-tdm-r2'] = self.getPackageList('http://downloads.sourceforge.net/sourceforge/mingw',
                                                        ['gcc-4.4.0-tdm-1-core-2.tar.gz',
                                                        'gcc-4.4.0-tdm-1-g++-2.tar.gz',
                                                        'binutils-2.18.50-20080109-2.tar.gz',
                                                        'mingw32-make-3.81-20080326.tar.gz',
                                                        'mingw-runtime-3.14.tar.gz',
                                                        'w32api-3.11.tar.gz',
                                                        'gdb-6.8-mingw-3.tar.bz2',
                                                        'mingw-utils-0.3.tar.gz'])
        self.targetMergePath['4.4.0-tdm-r2'] = "mingw";
		
        self.targets['4.4.0'] = self.getPackageList('http://downloads.sourceforge.net/sourceforge/mingw',
                                                 ['binutils-2.20.1-2-mingw32-bin.tar.gz',
                                                 'make-3.81-20090914-mingw32-bin.tar.gz',
                                                 'mingwrt-3.18-mingw32-dll.tar.gz',
                                                 'mingwrt-3.18-mingw32-dev.tar.gz',             
                                                 'w32api-3.14-mingw32-dev.tar.gz',
                                                 'gdb-7.0.50.20100202-mingw32-bin.tar.gz',
                                                 'mingw-utils-0.3.tar.gz',
                                                 'gcc-core-4.4.0-mingw32-bin.tar.gz',
                                                 'gcc-core-4.4.0-mingw32-dll.tar.gz',
                                                 'gcc-c++-4.4.0-mingw32-bin.tar.gz',
                                                 'gcc-c++-4.4.0-mingw32-dll.tar.gz',
                                                 'gmp-4.2.4-mingw32-dll.tar.gz',
                                                 'mpfr-2.4.1-mingw32-dll.tar.gz'])

        self.patchToApply['4.4.0']=('STRICT_ANSI.diff',0)
        self.targetMergePath['4.4.0'] = "mingw";

		
        self.defaultTarget = '4.4.0'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['gnuwin32/patch'] = 'default'
     
       
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)
        
    def install( self ):    
        shutil.copy( os.path.join( self.imageDir() , "bin", "mingwm10.dll" ), os.path.join( os.getenv( "KDEROOT" ) , "bin" , "mingwm10.dll" ) )
        return True

if __name__ == '__main__':
    Package().execute()
