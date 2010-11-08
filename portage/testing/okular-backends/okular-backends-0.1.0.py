import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['0.1.0'] = """http://winkde.org/pub/kde/ports/win32/repository/win32libs/libgs-GPL-8.63-bin.tar.bz2
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libgs-GPL-8.63-lib.tar.bz2

                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libspectre-0.2.1-bin.tar.bz2
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libspectre-0.2.1-lib.tar.bz2

                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/ebook-tools-0.1.0-bin.tar.bz2
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/ebook-tools-0.1.0-lib.tar.bz2
                                  
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libzip-0.8.0-bin.tar.bz2
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libzip-0.8.0-lib.tar.bz2"""
        self.targetInstSrc['0.1.0'] = ""
        self.defaultTarget = '0.1.0'

    def setDependencies( self ):
        """ """
        self.hardDependencies['virtual/bin-base'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.createCombinedPackage = True

if __name__ == '__main__':
    subclass().execute()
