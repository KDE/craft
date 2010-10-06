# -*- coding: utf-8 -*-
import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/koffice"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'
    
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
		defines = ""
        defines += "-DBUILD_karbon=OFF "
        defines += "-DBUILD_kpresenter=OFF "
        defines += "-DBUILD_kchart=OFF "
        defines += "-DBUILD_kdgantt=OFF "
        defines += "-DBUILD_kexi=OFF "
        defines += "-DBUILD_kivio=OFF "
        defines += "-DBUILD_kounavail=OFF "
        defines += "-DBUILD_kplato=OFF "
#        defines += "-DBUILD_krita=OFF "
        defines += "-DBUILD_kword=OFF "
        defines += "-DBUILD_kspread=OFF "
        defines += "-DBUILD_doc=OFF "

		self.subinfo.options.configure.defines = defines
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()