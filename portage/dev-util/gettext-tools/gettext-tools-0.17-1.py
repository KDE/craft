import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.17'] = 'http://winkde.org/pub/kde/ports/win32/repository/win32libs/gettext-tools-0.17-bin.tar.bz2'
        self.defaultTarget = '0.17'
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/gettext'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, "" )
        self.instdestdir = "dev-utils"
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
