#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# cvs support

from Source.VersionSystemSourceBase import *
from shells import *

## \todo requires installed git package -> add suport for installing packages

class CvsSource (VersionSystemSourceBase):
    """cvs support"""
    def __init__(self):
        VersionSystemSourceBase.__init__(self)

    def fetch( self, dummyRepopath=None ):
        utils.die("not implemented yet")

