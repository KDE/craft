#
# copyright (c) 2011 Ralf Habacker <ralf.habacker@freenet.de>
#

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.BuildSystemBase import *
from Packager.PackagerBase import *

class PythonPackageBase(PackageBase, MultiSource, BuildSystemBase, PackagerBase):
    def __init__( self ):
        utils.debug("PythonPackageBase.__init__ called", 2)
        PackageBase.__init__( self )
        MultiSource.__init__( self )
        BuildSystemBase.__init__( self )
        PackagerBase.__init__( self )
        
    def install( self ): 
        ret = self.system("cd %s && python setup.py install" % self.sourceDir() )
        print(ret)
        return True

    def unmerge( self ): 
        # setup.py do not support uninstalling 
        print("not supported yet")
        # we do not want to break unmerging other packages
        return True
