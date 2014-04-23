from Package.BinaryPackageBase import *
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for version in ['3.1.1']:
            self.targets[ version ] = "http://www.apache.org/dist/xerces/c/3/binaries/xerces-c-3.1.1-x86-windows-vc-10.0.zip"
        self.targetDigests['3.1.1'] = '34df759e1ffe4acce301887007cccb62f9496ea0'

        self.shortDescription = "A Validating XML Parser"
        self.defaultTarget = '3.1.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['win32libs/xerces-c'] = 'default'


class PackageBin(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.withSources = False

    def unpack( self ):
        if not BinaryPackageBase.unpack( self ): return False
        os.renames( os.path.join( self.imageDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "include" ), os.path.join( self.imageDir(), "include" ) )
        os.renames( os.path.join( self.imageDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "bin" ), os.path.join( self.imageDir(), "bin" ) )
        os.renames( os.path.join( self.imageDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "lib" ), os.path.join( self.imageDir(), "lib" ) )
        shutil.rmtree( os.path.join( self.imageDir(), "xerces-c-3.1.1-x86-windows-vc-10.0" ) )
        return True

from Package.VirtualPackageBase import *

if compiler.isMSVC():
    class Package(PackageBin):
        def __init__( self ):
            PackageBin.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )
            

if __name__ == '__main__':
      Package().execute()