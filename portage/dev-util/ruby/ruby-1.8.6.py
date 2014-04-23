import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.9.2'] = "ftp://ftp.ruby-lang.org/pub/ruby/binaries/mswin32/ruby-1.9.2-p136-i386-mswin32.zip"
        self.defaultTarget = '1.9.2'
        self.targetDigests['1.9.2'] = 'e8cbc6215d1f08433b105661a1ac72c197e2e5b1'
        self.targetMergePath['1.9.2'] = 'dev-utils'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

    def unpack(self):
        res = BinaryPackageBase.unpack( self )
        # ruby package contains a file called MANIFEST that we need to get
        # out of the way so we can make the manifest dir
        if res:
          os.remove( os.path.join( self.installDir(), "MANIFEST" ) )
        return res

if __name__ == '__main__':
    Package().execute()

