# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# cvs support

from VersionSystemSourceBase import *
import os
import utils
from shells import *

## \todo requires installed git package -> add suport for installing packages 

class CvsSource (VersionSystemSourceBase):
    """cvs support"""   
    def __init__(self):
        VersionSystemSourceBase.__init__(self)        

    def fetch( self, repopath=None, packagedir=None ):
        utils.die("not implemented yet")
            
