# -*- coding: utf-8 -*-
# Packager base

from EmergeBase import *

class PackagerBase(EmergeBase):
    """ provides a generic interface for packagers and implements basic package creating stuff """
    def __init__(self):
        EmergeBase.__init__(self)
    
    #""" create a package """
    def createPackage(self): abstract()

    # for compatibility 
    def make_package(self):
        return self.createPackage()



