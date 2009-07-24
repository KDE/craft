# -*- coding: utf-8 -*-
# git support

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
            
