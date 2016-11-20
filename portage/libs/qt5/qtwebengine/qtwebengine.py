# -*- coding: utf-8 -*-
import CraftDebug
import info


class subinfo(info.infoclass):
    def setTargets( self ):       
        self.versionInfo.setDefaultValues( )

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'


from Package.Qt5CorePackageBase import *

class Package( Qt5CorePackageBase ):
    def __init__( self, **args ):
        Qt5CorePackageBase.__init__( self )
        self.supportsNinja = False  # Includes its own ninja, not to be confused with ours
        self.subinfo.options.fetch.checkoutSubmodules = True
        
    def compile(self):
        if not ("Paths","Python27") in craftSettings:
            CraftDebug.die("Please make sure Paths/Python27 is set in your kdesettings.ini")
        utils.prependPath(craftSettings.get("Paths","PYTHON27",""))
        return Qt5CorePackageBase.compile(self)
       

        
