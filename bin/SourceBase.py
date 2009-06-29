# -*- coding: utf-8 -*-

from EmergeBase import *

class SourceBase(EmergeBase):
    """ implements basic stuff required for  all sources"""
    def __init__(self):
        EmergeBase.__init__(self)

    def fetch(self): abstract

    def unpack(self): abstract
