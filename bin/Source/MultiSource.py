# -*- coding: utf-8 -*-

import info
import utils

from SourceFactory import *

class MultiSource():
    """ provides multi source type api """
    def __init__(self):
        utils.debug( "MultiSource __init__", 1 )
        self.source = SourceFactory(self.subinfo)

    def fetch(self):
        return self.source.fetch()
        
    def unpack(self):
        return self.source.unpack()
