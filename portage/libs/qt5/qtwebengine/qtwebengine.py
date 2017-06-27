# -*- coding: utf-8 -*-
from CraftDebug import craftDebug
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

    def setDependencies( self ):
        self.buildDependencies['gnuwin32/gperf'] = 'default'
        self.buildDependencies['dev-util/python2'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtlocation'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtwebchannel'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        self.subinfo.options.fetch.checkoutSubmodules = True
        # sources on different partitions other than the one of the build dir
        # fails. some submodules fail even with the common shadow build...
        self.subinfo.options.useShadowBuild = False
        if CraftVersion(self.subinfo.buildTarget) >= CraftVersion("5.10"):
            craftDebug.log.warning("Please try to build QtWebengine useShadowBuild enabled")
            exit()

    def fetch(self):
        if isinstance(self.source, GitSource):
            self.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return Qt5CorePackageBase.fetch(self)
        
    def compile(self):
        utils.prependPath(craftSettings.get("Paths","PYTHON27"))
        return Qt5CorePackageBase.compile(self)
       

        
