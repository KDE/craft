# -*- coding: utf-8 -*-
import info
import platform
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['win32libs-sources/boost-src']   = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        
        self.hardDependencies['win32libs-bin/shared-mime-info'] = 'default'
        
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/sqlite-src'] = 'default'

    def setTargets( self ):
        self.svnTargets['0.80'] = 'tags/akonadi/0.80'
        self.svnTargets['0.81'] = 'tags/akonadi/0.81'
        self.svnTargets['0.82'] = 'tags/akonadi/0.82'
        self.svnTargets['1.0.0'] = 'tags/akonadi/1.0.0'
        self.svnTargets['1.0.80'] = 'tags/akonadi/1.0.80'
        self.svnTargets['1.1.0']  = 'tags/akonadi/1.1.0'
        self.svnTargets['1.1.1']  = 'tags/akonadi/1.1.1'
        self.svnTargets['1.1.2']  = 'tags/akonadi/1.1.2'
        self.svnTargets['1.1.3']  = 'tags/akonadi/1.1.3'
        self.svnTargets['1.3.1']  = 'tags/akonadi/1.3.1'
        for i in ['4.3.0', '4.3.1', '4.3.2', '4.3.3', '4.3.4', '4.3']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.3/kdesupport/akonadi'
        for i in ['4.5.0', '4.5']:
            self.svnTargets[ i ] = 'tags/kdesupport-for-4.5/kdesupport/akonadi'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/akonadi'
        self.svnTargets['gitHEAD'] = 'git://git.kde.org/akonadi.git'
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines  = " -DCMAKE_PROGRAM_PATH=%s " % os.path.join( os.getenv("KDEROOT") , "dev-utils" , "svn" , "bin" )
        if platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += " -DINSTALL_QSQLITE_IN_QT_PREFIX=TRUE "
            self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
                % os.path.join(ROOTDIR, "bin")

        if self.isTargetBuild():
            automoc = os.path.join(self.rootdir, "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                print("<%s>") % automoc
                utils.die("could not find automoc")
            self.subinfo.options.configure.defines += "-DDATABASE_BACKEND=SQLITE -DAKONADI_STATIC_SQLITE=TRUE "
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += "-DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
