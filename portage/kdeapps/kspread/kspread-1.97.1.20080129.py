import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/koffice"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['win32libs-bin/lcms'] = 'default'
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.buildDependencies['kdesupport/eigen2'] = 'default'
#        self.dependencies['testing/gsl'] = 'default'
    

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        defines = ""
        defines += "-DBUILD_karbon=OFF "
        defines += "-DBUILD_kpresenter=OFF "
        defines += "-DBUILD_kchart=OFF "
        defines += "-DBUILD_kdgantt=OFF "
        defines += "-DBUILD_kexi=OFF "
        defines += "-DBUILD_kivio=OFF "
        defines += "-DBUILD_kounavail=OFF "
        defines += "-DBUILD_kplato=OFF "
        defines += "-DBUILD_krita=OFF "
        defines += "-DBUILD_kword=OFF "
#        defines += "-DBUILD_kspread=OFF "
        defines += "-DBUILD_doc=OFF "
		self.subinfo.options.configure.defines = defines

if __name__ == '__main__':
    Package().execute()