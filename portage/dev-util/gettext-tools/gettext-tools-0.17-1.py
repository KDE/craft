import gnuwin32
import info

DEPEND = """

"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.17'] = 'http://winkde.org/pub/kde/ports/win32/repository/win32libs/gettext-tools-0.17-bin.tar.bz2'
        self.defaultTarget = '0.17'
    def setDependencies( self ):
        self.hardDependencies['dev-util/win32libs'] = 'default'

class subclass(gnuwin32.gnuwin32class):
    def __init__( self, **args ):
        gnuwin32.gnuwin32class.__init__( self, SRC_URI )
        self.subinfo = subinfo()

if __name__ == '__main__':
    subclass().execute()
