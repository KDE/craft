# -*- coding: utf-8 -*-
# KOffice trunk with kdelibs and kdelibs trunk
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
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "koffice"
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_karbon=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kformula=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kpresenter=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kchart=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kdgantt=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kexi=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kivio=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kounavail=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kplato=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_krita=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kword=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kspread=OFF "
#        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_doc=OFF "

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "koffice" )

if __name__ == '__main__':
    subclass().execute()
