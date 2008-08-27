import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        """ """
        self.targets['0.2.1'] = """http://winkde.org/pub/kde/ports/win32/repository/win32libs/libspectre-0.2.1-bin.tar.bz2
                                  http://winkde.org/pub/kde/ports/win32/repository/win32libs/libspectre-0.2.1-lib.tar.bz2"""
        self.targetInstSrc['0.2.1'] = ""
        self.defaultTarget = '0.2.1'

    def setDependencies( self ):
        """ """
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.createCombinedPackage = True

if __name__ == '__main__':
    subclass().execute()
