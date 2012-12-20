# uactools : Binary package of the tools to handle UAC from kde-windows.
# mt.exe can be used to embed manifest files to disable heuristic UAC raise
# requests, setuac.exe can be used to enable raise the privileges of a program.
# The according source package is uactools-pkg


import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ "1.2" ] = "http://downloads.sourceforge.net/winflexbison/win_flex_bison-1.2.zip"
        self.targetDigests['1.2'] = 'e8896393f4a4e196f23a1f017f2a1c1d1b290f5a'
        self.defaultTarget = "1.2"

    def setDependencies( self ):
        self.buildDependencies['gnuwin32/wget'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.install.installPath = "bin"
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
