import os

import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['dev-util/msys'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://repo.or.cz/git-cheetah'

        self.defaultTarget = 'gitHEAD'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        self.buildInSource = True
        self.makeProgram = "make"
        utils.prependPath(os.path.join( emergeRoot() , "dev-utils" , "git" , "bin" ))
        
    def configure(self):
        return True
      
    def install(self):
        utils.copyFile(os.path.join(self.sourceDir() , "explorer" , "git_shell_ext.dll" ) , os.path.join( self.imageDir() , "bin" , "git_shell_ext.dll" ))
        return True
        
    def qmerge(self):
        if not AutoToolsPackageBase.qmerge(self):
            return False
        utils.system("regsvr32 -s -n -i:machine %s" % utils.deSubstPath(os.path.join(self.mergeDestinationDir() , "bin" , "git_shell_ext.dll" )))
        return True
        
    def unmerge(self):
        utils.system("regsvr32 -u -s -n -i:machine %s" % utils.deSubstPath(os.path.join(self.mergeDestinationDir() , "bin" , "git_shell_ext.dll" )))
        return AutoToolsPackageBase.unmerge(self)
        
