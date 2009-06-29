# -*- coding: utf-8 -*-

import os;

class EmergeBase():
    """base class for emerge system - holds attributes and methods required by base classes"""
    # todo refactor initialisation 
    ROOTDIR=os.getenv( "KDEROOT" )
    rootdir=ROOTDIR 

    # todo from base.py, used by gitsource
    DOWNLOADDIR=os.getenv( "DOWNLOADDIR" )
    downloaddir = DOWNLOADDIR
    
    def __init__(self):
        dummy = 0

    def abstract():
        import inspect
        caller = inspect.getouterframes(inspect.currentframe())[1][3]
        raise NotImplementedError(caller + ' must be implemented in subclass')
