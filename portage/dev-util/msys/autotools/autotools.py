import info


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = "20100923"
        self.targets[ ver ] = "http://downloads.sourceforge.net/sourceforge/mingw-w64/autotools-" + ver + ".tar.xz"
        self.targetDigests[ ver ] = '73fe57bec9f3813556a38602daf4e9ea9b4b0dba'

        self.defaultTarget = ver

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['dev-util/7zip'] = 'default'
        self.dependencies['dev-util/minsys'] = 'default'
        self.dependencies['dev-util/libtool'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "msys/opt"

if __name__ == '__main__':
    Package().execute()
