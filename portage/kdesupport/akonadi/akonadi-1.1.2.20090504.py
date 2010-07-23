# -*- coding: utf-8 -*-
import info
import platform
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['win32libs-bin/boost']   = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        
        self.hardDependencies['win32libs-bin/shared-mime-info'] = 'default'
        
        if not platform.isCrossCompilingEnabled():
            self.boostversion = "1.37"
        else:
            self.hardDependencies['win32libs-sources/sqlite-src'] = 'default'
            self.boostversion = "1.40.0"

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
        self.defaultTarget = 'svnHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines  = " -DCMAKE_PROGRAM_PATH=%s " % os.path.join( os.getenv("KDEROOT") , "dev-utils" , "svn" , "bin" )
        self.subinfo.options.configure.defines += " -DBoost_ADDITIONAL_VERSIONS=" + self.subinfo.boostversion
        if not platform.isCrossCompilingEnabled():
            self.boost = portage.getPackageInstance("win32libs-bin","boost")
        else:
            self.boost = portage.getPackageInstance("win32libs-sources","boost-src")
        self.subinfo.options.configure.defines += " -DBoost_INCLUDE_DIR=" + os.path.join(self.boost.mergeDestinationDir(), "include", "boost-" + self.subinfo.boostversion.replace(".", "_") )
        if platform.isCrossCompilingEnabled():
            os.environ["BOOST_LIBRARYDIR"]  = os.path.join(self.boost.mergeDestinationDir(), "lib", "boost-" + self.subinfo.boostversion.replace(".", "_") )
        self.subinfo.options.configure.defines += " -DINSTALL_QSQLITE_IN_QT_PREFIX=TRUE "
            
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")
            
        if self.isTargetBuild():
            automoc = os.path.join(self.rootdir, "lib", "automoc4", "Automoc4Config.cmake")
            if not os.path.exists(automoc):
                print("<%s>") % automoc
                utils.die("could not found automoc")
            ## \todo a standardized way to check if a package is installed in the image dir would be good.
            self.subinfo.options.configure.defines += "-DAUTOMOC4_CONFIG_FILE:FILEPATH=%s " \
                % automoc.replace('\\', '/')

if __name__ == '__main__':
    Package().execute()
