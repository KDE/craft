import info

## package info implementation 
class subinfo(info.infoclass):

    ## define targets
    def setTargets( self ):
        ## todo add doc 
        self.targets['default'] = 'http://www.winkde.org/pub/kde/ports/win32/repository/gnuwin32/libbzip2-1.0.5-1-bin.tar.bz2'
       
        ## todo add doc 
        #self.targetInstSrc['default'] = 'bzip2-1.0.4'

        ## todo add doc 
        #self.targetMergeSourcePath['default'] = 'bin'

        ## todo add doc 
        #self.targetMergePath['default'] = 'dev-utils'
        
        ## todo add doc 
        self.defaultTarget = 'default'
    
    ## define dependencies
    #def setDependencies( self ):
    #    self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
from Package.BinaryPackageBase import *
                
## package implementation
class Package(BinaryPackageBase):
    def __init__( self ):
        # instantiate subinfo class
        self.subinfo = subinfo()
        # call base constructor 
        BinaryPackageBase.__init__(self)

   ## for nonstandard fetch operation
    # the files will be fetched info self.sourceDir() 
	#
    #def fetch(self):
    #    #do something before fetching
    #    if not CMakePackageBase.fetch(self):
    #        return False
    #    #do something after fetching
	#    return True
    
    ## for nonstandard unpack operation
    # the files will be read from self.downloadDir() 
    # and unpacked into self.sourceDir()
	#
    #def unpack(self):
    #    #do something before unpack
    #    if not CMakePackageBase.unpack(self):
    #        return False
    #    #do something after unpack
	#    return True

    ## for nonstandard configure operation
	# self.sourceDir() will be used for accessing source files 
	# and self.buildDir() for storing build files 
	# 
    #def configure(self):
    #    #do something before configure
    #    if not CMakePackageBase.configure(self):
    #        return False
    #    #do something after configure
	#    return True

    ## for nonstandard make operation
	#  uses self.buildDir() to access build files
	# 
    #def make(self):
    #    #do something before make
    #    if not CMakePackageBase.make(self):
    #        return False
    #    #do something after make
	#    return True
	
    ## for nonstandard install operation
    # the installed files will be installed 
	# into self.installDir()
	#
    #def install(self):
    #    #do something before install
    #    if not CMakePackageBase.install(self):
    #        return False
    #    #do something after install
	#    return True
	
	## for  nonstandard merge operation
	# the files are taken from self.installDir()
	# and merged into self.mergeDestinationDir()
	# 
    #def qmerge(self):
    #    #do something before merging
    #    if not CMakePackageBase.qmerge(self):
    #        return False
    #    #do something after merging
	#    return True
    
	## for  nonstandard unmerge operation
	# the related files are removed from 
	# self.mergeDestinationDir()
	# 
    #def unmerge(self):
    #    #do something before unmerging
    #    if not CMakePackageBase.unmerge(self):
    #        return False
    #    #do something after unmerging
	#    return True

	## for nonstandard directions operations 
	# 
	#def sourceDir(self):
	#    # get standard source path  
    #    dir = CMakePackageBase.sourceDir(self):
	# 	 #do something with path 
	# 	 return dir

	# the same belongs to the following methods 
    #def downloadDir(self): 
    #def packageDir(self): 
    #def filesDir(self):
    #def buildRoot(self):
    #def workDir(self):
    #def buildDir(self):        
    #def imageDir(self):
    #def installDir(self):
    #def mergeDestinationDir(self):
	
    
if __name__ == '__main__':
    Package().execute()
