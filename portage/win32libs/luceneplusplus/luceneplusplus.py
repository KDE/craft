import info


class subinfo (info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/boost-thread'] = 'default'
        self.dependencies['win32libs/boost-system'] = 'default'
        self.dependencies['win32libs/boost-regex'] = 'default'
        self.dependencies['win32libs/boost-iostreams'] = 'default'
        self.dependencies['win32libs/boost-date-time'] = 'default'
        self.dependencies['win32libs/boost-filesystem'] = 'default'


    def setTargets( self ):
        # for ver in [ "3.0.6" ]:
        #     self.targets[ ver ] = "https://github.com/luceneplusplus/LucenePlusPlus/archive/rel_%s.tar.gz" % ver
        #     self.archiveNames[ ver ] = "luceneplusplus-%s.tar.gz" % ver
        #     self.targetInstSrc[ ver ] = "LucenePlusPlus-rel_%s" % ver
        # self.targetDigests['3.0.6'] = 'a4504f82075bf715a156e8e81404758ddf5e44b0'

        self.svnTargets[ "gitHEAD" ] = "https://github.com/luceneplusplus/LucenePlusPlus.git"
        
        self.shortDescription = "Lucene++ is an up to date C++ port of the popular Java Lucene library, a high-performance, full-featured text search engine."
        self.homepage = "https://github.com/luceneplusplus/LucenePlusPlus/"
        self.defaultTarget = "gitHEAD"


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DENABLE_TEST=OFF"
