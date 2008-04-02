import base
import info

PACKAGE_NAME         = "boost-jam"
PACKAGE_VER          = "3.1.16"
PACKAGE_FULL_VER     = "3.1.16-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER)

SRC_URI= """
http://downloads.sourceforge.net/boost/""" + PACKAGE_FULL_NAME + """-ntx86.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.1.16-1'] = SRC_URI
        self.targetInstSrc['3.1.16-1'] = PACKAGE_FULL_NAME + "-ntx86"
        self.defaultTarget = '3.1.16-1'
    
    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        if self.traditional:
            self.instdestdir = "bjam\bin"
        else:
            self.instdestdir = "bin"
        self.subinfo = subinfo()

    def make_package( self ):
        if self.traditional:
            self.instdestdir = "bjam"
        else:
            self.instdestdir = ""
        return self.doPackaging( PACKAGE_NAME, PACKAGE_VER, True )

if __name__ == '__main__':
    subclass().execute()
