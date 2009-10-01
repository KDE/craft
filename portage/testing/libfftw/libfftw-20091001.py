# -*- coding: utf-8 -*-
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.3.2'] = 'ftp://ftp.fftw.org/pub/fftw/fftw-3.2.2.pl1-dll32.zip'
        self.defaultTarget = '3.3.2'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        

from Package.BinaryPackageBase import *
        
class Package(BinaryPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__(self)

    def __move(self, filenames, destdir):
        """ check if the destination directory exists and move multiple files """
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for i in filenames:
            shutil.move(os.path.join(self.imageDir(), i), os.path.join(destdir, i))

        
    def unpack(self):
        BinaryPackageBase.unpack(self)
        self.__move('bench.exe benchf.exe benchl.exe fftw-wisdom.exe fftwf-wisdom.exe fftwl-wisdom.exe libfftw3-3.dll libfftw3f-3.dll libfftw3l-3.dll'.split(), os.path.join(self.imageDir(), "bin"))
        self.__move('libfftw3-3.def libfftw3f-3.def libfftw3l-3.def'.split(), os.path.join(self.imageDir(), "lib"))
        self.__move('fftw3.f fftw3.h'.split(), os.path.join(self.imageDir(), "include"))
        self.__move('COPYING COPYRIGHT NEWS README README-bench README-WINDOWS'.split(), os.path.join(self.imageDir(), "doc", "fftw"))

        for i in "libfftw3-3 libfftw3f-3 libfftw3l-3".split():
            utils.createImportLibs(i, self.imageDir())
        return True

if __name__ == '__main__':
    Package().execute()
